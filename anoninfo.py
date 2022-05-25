__version__ = (0, 0, 49)


# ▄▀█ █▄░█ █▀█ █▄░█ █▀▄ ▄▀█ █▀▄▀█ █░█ █▀
# █▀█ █░▀█ █▄█ █░▀█ █▄▀ █▀█ █░▀░█ █▄█ ▄█
#
#              © Copyright 2022
#
# https://t.me/apodiktum_modules | https://t.me/hikariatama
#
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @anon97945 | @hikariatama

# scope: inline
# scope: hikka_only
# scope: hikka_min 1.1.27

import logging
import git

from telethon.tl.types import Message
from telethon.utils import get_display_name

from .. import loader, main, utils
from ..inline.types import InlineQuery

logger = logging.getLogger(__name__)


@loader.tds
class anoninfoMod(loader.Module):
    """Показывает информацию о юзерботе"""

    strings = {
        "name": "AnonInfo",
        "owner": "Владелец",
        "version": "Версия",
        "build": "Сборка",
        "prefix": "Префикс",
        "up-to-date": "😌 Актуальная версия",
        "update_required": "😕 Требуется обновление </b><code>.update</code><b>",
        "_cfg_cst_msg": "Кастомный текст сообщения в info. Может содержать ключевые слова {me}, {version}, {build}, {prefix}, {platform}",
        "_cfg_cst_btn": "Кастомная кнопка в info. Оставь пустым, чтобы убрать кнопку",
        "_cfg_cst_bnr": "Кастомный баннер в info",
        "_cfg_cst_frmt": "Кастомный формат файла для баннера в info",
        "_cfg_banner": "Поставь `True`, чтобы отключить баннер с изображением",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                "no",
                doc=lambda: self.strings("_cfg_cst_msg"),
            ),
            loader.ConfigValue(
                "custom_button1",
                ["🔥 Apodiktum Hikka Modules 🔥", "https://t.me/apodiktum_modules"],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2, doc=ru),
            ),
            loader.ConfigValue(
                "custom_button2",
                ["🌘 Hikka RU Support chat", "https://t.me/hikka_talks"],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_button3",
                ["🌘 Hikka EN Support chat", "https://t.me/hikka_en"],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_banner",
                "https://i.ibb.co/BZ9Kg2N/Banner.png",
                lambda: self.strings("_cfg_cst_bnr"),
            ),
            loader.ConfigValue(
                "disable_banner",
                False,
                lambda: self.strings("_cfg_banner"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "custom_format",
                "photo",
                lambda: self.strings("_cfg_cst_frmt"),
                validator=loader.validators.Choice(["photo", "video", "audio", "gif"]),
            ),
        )

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._me = await client.get_me()

    def _render_info(self) -> str:
        ver = utils.get_git_hash() or "Unknown"

        try:
            repo = git.Repo()
            diff = repo.git.log(["HEAD..origin/master", "--oneline"])
            upd = (
                self.strings("update_required") if diff else self.strings("up-to-date")
            )
        except Exception:
            upd = ""

        me = f'<b><a href="tg://user?id={self._me.id}">{utils.escape_html(get_display_name(self._me))}</a></b>'
        version = f'<i>{".".join(list(map(str, list(main.__version__))))}</i>'
        build = f'<a href="https://github.com/hikariatama/Hikka/commit/{ver}">#{ver[:8]}</a>'  # fmt: skip
        prefix = f"«<code>{utils.escape_html(self.get_prefix())}</code>»"
        platform = utils.get_named_platform()

        return (
            "<b>😈 Anondamus Hikka Info</b>\n"
            + self.config["custom_message"].format(
                me=me,
                version=version,
                build=build,
                prefix=prefix,
                platform=platform,
            )
            if self.config["custom_message"] != "no"
            else (
                "<b>😈 Anondamus Hikka Info</b>\n"
                f'<b>🤴 {self.strings("owner")}: </b>{me}\n\n'
                f"<b>🔮 {self.strings('version')}: </b>{version} {build}\n"
                f"<b>{upd}</b>\n\n"
                f"<b>📼 {self.strings('prefix')}: </b>{prefix}\n"
                f"<b>{platform}</b>\n"
            )
        )

    def _get_mark(self, int):
        if int == 1:
            return (
                {
                    "text": self.config["custom_button1"][0],
                    "url": self.config["custom_button1"][1],
                }
                if self.config["custom_button1"]
                else None
            )

        elif int == 2:
            return (
                {
                    "text": self.config["custom_button2"][0],
                    "url": self.config["custom_button2"][1],
                }
                if self.config["custom_button2"]
                else None
            )

        elif int == 3:
            return (
                {
                    "text": self.config["custom_button3"][0],
                    "url": self.config["custom_button3"][1],
                }
                if self.config["custom_button3"]
                else None
            )

    @loader.unrestricted
    async def anoninfocmd(self, message: Message):
        """Отправить информацию о юзерботе"""
        m1 = self._get_mark(1)
        m2 = self._get_mark(2)
        m3 = self._get_mark(3)
        await self.inline.form(
            message=message,
            text=self._render_info(),
            reply_markup=[
                [
                    *([m1] if m1 else []),
                ],
                [
                    *([m2] if m2 else []),
                    *([m3] if m3 else []),
                ],
            ],
            **{}
            if self.config["disable_banner"]
            else {self.config["custom_format"]: self.config["custom_banner"]}
        )
