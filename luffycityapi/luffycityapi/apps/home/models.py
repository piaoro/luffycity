from luffycityapi.utlis.models import BaseModel, models


class Nav(BaseModel):
    POSITION_CHOICE = (
        (0, "顶部导航"),
        (1, "脚部导航")
    )

    link = models.CharField(max_length=255, verbose_name="导航链接")
    is_http = models.BooleanField(default=False, verbose_name="是否是外部链接")
    position = models.SmallIntegerField(default=0, choices=POSITION_CHOICE, verbose_name="导航位置")

    class Meta:
        db_table = "fg_nav"
        verbose_name = "导航菜单"
        verbose_name_plural = verbose_name
