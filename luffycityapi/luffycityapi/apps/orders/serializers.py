from datetime import datetime
from rest_framework import serializers
from django_redis import get_redis_connection
from .models import Order, OrderDetail, Course
from django.db import transaction
from coupon.models import CouponLog
import logging
from luffycityapi.utlis import constants

logger = logging.getLogger("django")


class OrderModelSerializer(serializers.ModelSerializer):
    pay_link = serializers.CharField(read_only=True)
    user_coupon_id = serializers.IntegerField(write_only=True, default=-1)

    class Meta:
        model = Order
        fields = ['pay_type', 'id', 'order_number', 'pay_link', 'user_coupon_id', 'credit']
        read_only_fields = ['id', 'order_number']
        extra_kwargs = {
            "pay_type": {"write_only": True},
            "credit": {"writer_only": True},
        }

    def create(self, validated_data):
        """创建订单"""
        redis = get_redis_connection("cart")
        user = self.context["request"].user
        user_id = user.id
        # 判断用户如果使用了优惠券，则优惠券需要判断验证
        user_coupon_id = validated_data.get("user_coupon_id")
        user_coupon = None
        if user_coupon_id != -1:
            user_coupon = CouponLog.objects.filter(pk=user_coupon_id, user_id=user_id).first()

        # 本次下单时使用的积分数量
        use_credit = validated_data.get("credit")
        if use_credit > 0 and use_credit > user.credit:
            raise serializers.ValidationError(detail="您拥有的积分不足以抵扣本次下单的积分，请重新下单！")

        # 开启事务操作，保证下单过程中的所有数据库的原子性
        with transaction.atomic():
            # 设置事务的回滚点标记
            t1 = transaction.savepoint()
            try:
                # 创建订单记录
                order = Order.objects.create(
                    name="购买课程",  # 订单标题
                    user_id=user_id,
                    # order_number = datetime.now().strftime("%Y%m%d%H%M%S") + ("%08d" % user_id) + "%08d" % random.randint(1,99999999) # 基于随机数生成唯一订单号
                    order_number=f"{datetime.now().strftime('%Y%m%d')}{user_id:08d}{redis.incr('order_number')}",
                    # 基于redis生成分布式唯一订单号
                    pay_type=validated_data.get("pay_type")  # 支付方式
                )

                # 记录本次下单的商品列表
                cart_hash = redis.hgetall(f"cart_{user_id}")
                if len(cart_hash) < 1:
                    raise serializers.ValidationError(detail="购物车没有商品")

                # 提取购物车中所有勾选状态为b'1'的商品
                course_id_list = [int(key.decode()) for key, value in cart_hash.items() if value == b'1']

                # 添加订单与课程的关系
                course_list = Course.objects.filter(pk__in=course_id_list, is_delete=False, is_show=True).all()
                detail_list = []
                total_price = 0  # 本次订单的总价格
                real_price = 0  # 本次订单的实付总价

                # 用户使用优惠券或积分以后，需要在服务端计算本次使用优惠券或积分的最大优惠额度
                total_discount_price = 0  # 总优惠价格
                max_discount_course = None  # 享受最大优惠的课程

                # 本次下单最多可以抵扣的积分
                max_use_credit = 0

                for course in course_list:
                    discount_price = course.discount.get("price", None)  # 获取课程折扣价
                    if discount_price is not None:
                        discount_price = float(discount_price)
                    discount_name = course.discount.get("type", "")
                    detail_list.append(OrderDetail(
                        order=order,
                        course=course,
                        name=course.name,
                        price=course.price,
                        real_price=course.price if discount_price is None else discount_price,
                        discount_name=discount_name,
                    ))

                    # 统计订单的总价和实付总价
                    total_price += float(course.price)
                    real_price += float(course.price if discount_price is None else discount_price)

                    # 在用户使用了优惠券，并且当前课程没有参与其他优惠活动时，找到最佳优惠课程
                    if user_coupon_id and discount_price is None:
                        if max_discount_course is None:
                            max_discount_course = course
                        else:
                            if course.price >= max_discount_course.price:
                                max_discount_course = course

                    # 添加每个课程的可用积分
                    if use_credit > 0 and course.credit > 0:
                        max_use_credit += course.credit

                    # 在用户使用了优惠券以后，根据循环中得到的最佳优惠课程进行计算最终抵扣金额
                    if user_coupon:
                        # 优惠公式
                        sale = float(user_coupon.coupon.sale[1:])
                        if user_coupon.coupon.discount == 1:
                            """减免优惠券"""
                            total_discount_price = sale
                        elif user_coupon.coupon.discount == 2:
                            """折扣优惠券"""
                            total_discount_price = float(max_discount_course.price) * (1 - sale)

                    if use_credit > 0:
                        if max_use_credit < use_credit:
                            raise serializers.ValidationError(detail="本次使用的抵扣积分数额超过了限制！")
                        # 当前订单添加积分抵扣的数量
                        order.credit = use_credit
                        total_discount_price = float(use_credit / constants.CREDIT_TO_MONEY)
                        # todo 扣除用户拥有的积分，后续在订单超时未支付，则返还订单中对应数量的积分给用户。如果订单成功支付，则添加一个积分流水记录。
                        user.credit = user.credit - use_credit
                        user.save()
                # 一次性批量添加本次下单的商品记录
                OrderDetail.objects.bulk_create(detail_list)

                # 保存订单的总价格和实付价格
                order.total_price = total_price
                order.real_price = float(real_price - total_discount_price)
                order.save()

                # todo 支付链接地址[后面实现支付功能的时候，再做]
                order.pay_link = ""
                # 删除购物车中被勾选的商品，保留没有被勾选的商品信息
                cart = {key: value for key, value in cart_hash.items() if value == b'0'}

                pipe = redis.pipeline()
                pipe.multi()
                # 删除原来的购物车
                pipe.delete(f"cart_{user_id}")
                if cart:
                    # 重新把未勾选的商品记录到购物车中
                    pipe.hmset(f"cart_{user_id}", cart)
                pipe.execute()

                if user_coupon:
                    user_coupon.order = order
                    user_coupon.save()
                    # 把优惠券从redis中移除
                    redis = get_redis_connection("coupon")
                    redis.delete(f"{user_id}:{user_coupon_id}")
                return order
            except Exception as e:
                # 1. 记录日志
                logger.error(f"订单创建失败：{e}")
                # 2. 事务回滚
                transaction.savepoint_rollback(t1)
                # 3. 抛出异常，通知视图返回错误提示
                raise serializers.ValidationError(detail="订单创建失败")
