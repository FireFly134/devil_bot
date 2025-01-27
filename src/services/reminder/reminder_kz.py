"""Напоминалка по подпискам"""
import logging
from datetime import datetime, timedelta

from sqlalchemy import and_
from services.send_message import send_msg, send_msg_mv2
from tables.clans import Clans
from tables.heroes_of_users import HeroesOfUsers
from tables.telegram_users import User
from tables.text_table import TextTable

async def reminder_kz():
    time = datetime.now()
    time_kz = time + timedelta(hours=1)
    info_kz = await (HeroesOfUsers.select().join(User).where(
        and_(
            HeroesOfUsers.time_change_kz == int(time_kz.strftime('%H')),
            HeroesOfUsers.subscription_rock == True,
        )
    ).with_only_columns(
        (
            HeroesOfUsers.id,
            HeroesOfUsers.name,
            User.user_id
        )
    ).gino.all())
    info_kz_info = await HeroesOfUsers.query.where(
        and_(
            HeroesOfUsers.time_change_kz == int(time.strftime('%H')),
            HeroesOfUsers.rock > 0,
            HeroesOfUsers.description_of_the_kz,
        )
    ).with_only_columns(
        (
            HeroesOfUsers.id,
            HeroesOfUsers.name,
            User.user_id
        )
    ).gino.all()
    info_clans_kz = await Clans.query.where(
        and_(
            Clans.start,
            Clans.chat_id is not None,
            Clans.subscription_rock,
            Clans.time_kz == int(time_kz.strftime('%H')),
        )
    ).gino.all()

    info_clans_description_of_the_kz = await Clans.query.where(
        and_(
            Clans.start,
            Clans.chat_id is not None,
            Clans.description_of_the_kz,
            Clans.time_kz == int(time_kz.strftime('%H')),
        )
    ).gino.all()

    ### Напоминание в личку про смену КЗ ###
    if info_kz:
        logging.info(f"info_kz GO = {len(info_kz)}")
        for hero in info_kz:
            await send_msg(user_id=hero.user_id, text=f"До смены кланового задания остался 1 час! ({hero.name})")
            logging.info(f"info_kz hero.id = {hero.id}")

    if info_kz_info:
        logging.info(f"info_kz_info GO = {len(info_kz_info)}")
        text_info = TextTable.query.where(TextTable.name_text == int(time.strftime('%w'))).gino.first()
        if text_info:
            for hero in info_kz_info:
                name = str(hero.name).replace('_', '\_').replace('*', '\*').replace('[', '\[').replace(']', '\]').replace('(', '\(').replace(')', '\)').replace('`', '\`').replace('~', '\~').replace('>', '\>').replace('#', '\#').replace('+', '\+').replace('=', '\=').replace('-', '\-').replace('|', '\|').replace('{', '\{').replace('}', '\}').replace('.', '\.').replace('!', '\!')
                await send_msg(user_id=hero.user_id, text=f"{name}\!\n{text_info.text}")
                logging.info(f"info_kz_info hero.id = {hero.id}")

    ### Напоминание в чат про смену КЗ ###
    if info_clans_kz:
        logging.info(f"info_clans_kz GO = {len(info_clans_kz)}")
        for clan in info_clans_kz:
            await send_msg(user_id=clan.chat_id, text="До смены кланового задания остался 1 час!")
            logging.info(f"info_clans_kz clan.id = {clan.id}")

    ### Описание нового КЗ в чат ###
    if info_clans_description_of_the_kz:
        logging.info(f"info_clans_description_of_the_kz GO = {len(info_clans_description_of_the_kz)}")
        text_info = TextTable.query.where(TextTable.name_text == int(time.strftime('%w'))).gino.first()
        for clan in info_clans_description_of_the_kz.iterrows():
            await send_msg_mv2(user_id=clan.chat_id, text=text_info.text)
            logging.info(f"info_clans_description_of_the_kz clan.id = {clan.id}")
