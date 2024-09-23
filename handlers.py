from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

from fsm import PatientFSM
from validators import validate_name, validate_birthdate

patients = []

router = Router()

@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я бот для учета пациентов. Используйте /add для добавления пациента.\n"
        "Используйте /today для просмотра списка пациентов.\n"
        "Используйте /weekly_stats для просмотра статистики за неделю.\n"
    )


@router.message(Command('add'))
async def add_patient(message: types.Message, state: FSMContext):
    await state.set_state(PatientFSM.name)
    await message.answer("Введите ФИО пациента:")


@router.message(PatientFSM.name)
async def process_name(message: types.Message, state: FSMContext):
    if not validate_name(message.text):
        print('asdasd')
        await message.answer("Некорректное ФИО. Попробуйте снова.")
        return
    await state.update_data(name=message.text)
    await state.set_state(PatientFSM.birthdate)
    await message.answer("Введите дату рождения (в формате YYYY-MM-DD):")


@router.message(PatientFSM.birthdate)
async def process_birthdate(message: types.Message, state: FSMContext):
    if not validate_birthdate(message.text):
        await message.answer("Некорректная дата рождения. Попробуйте снова.")
        return
    await state.update_data(birthdate=message.text)
    data = await state.get_data()
    name = data['name']
    birthdate = data['birthdate']
    patients.append({
        'name': name,
        'birthdate': birthdate,
        'visit_date': datetime.now().date()
    })

    await state.clear()
    await message.answer("Пациент успешно добавлен!")


@router.message(Command('today'))
async def list_patients_today(message: types.Message):
    today = datetime.now().date()
    today_patients = [p['name'] for p in patients if p['visit_date'] == today]
    if today_patients:
        await message.answer("\n".join(today_patients))
    else:
        await message.answer("Сегодня пациентов не было.")


@router.message(Command('weekly_stats'))
async def weekly_stats(message: types.Message):
    stats = {day: 0 for day in range(7)}
    for patient in patients:
        delta = datetime.now().date() - patient['visit_date']
        if delta.days < 7:
            stats[delta.days] += 1
    response = "\n".join(
        [f"{(datetime.now() - timedelta(days=day)).strftime('%A')}: {count}" for day, count in stats.items()])
    await message.answer(response)
