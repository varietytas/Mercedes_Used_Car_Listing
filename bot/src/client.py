from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import config as cfg
from io import BytesIO
import keyboards as kb
from os import path
from PIL import Image
import requests


# Create a bot and Dispatcher object to process incoming updates
bot = Bot(cfg.API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# STATES
class FSMClient(StatesGroup):
    general_state = State()
    years_input = State() # for 'Mean price over years' request


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    with open(path.join('.', 'welcome_message.txt')) as f:
        m = f.read()
    await message.answer(m, reply_markup=kb.general_keyboard)
    await FSMClient.general_state.set()


@dp.message_handler(text=['/structure', '/descriptive_statistics', '/model_popularity',
                            '/cea', '/bubble_colored', '/fueltype_vs_mpg',
                            '/correlation_heatmap', '/hypothesis', 'Structure'],
                    state=FSMClient.general_state)
async def general(message: types.Message):
    '''General handler for data requests,
    substitute filenames from commands to URL'''

    m = message.text.lower()
    request = m[1:] if m[0] == '/' else m

    # Construct URLs to get files from server
    url_img = f'{cfg.REQUEST_URL}{request}?type=0'
    url_txt = f'{cfg.REQUEST_URL}{request}?type=1'

    # Get necessary image, write it to the 'temp' folder
    img = Image.open(
        BytesIO(requests.get(url_img).content), formats=['png']
    )
    img_path = path.join('..', 'temp', f'{request}.png')
    img.save(img_path)

    # Get necessary text
    text = requests.get(url_txt).text

    # Send the image and text to user
    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile(img_path),
        caption=text,
        reply_markup=kb.general_keyboard
    )


@dp.message_handler(text=['/overview', 'Overview'],
                    state=FSMClient.general_state)
async def overview(message: types.Message):
    '''The handler for overview stands out as two messages
    (two photos and two captions) need to be send for one command'''

    # Construct URLs to get files from server
    url_img_ov = f'{cfg.REQUEST_URL}overview?type=0'
    url_txt_ov = f'{cfg.REQUEST_URL}overview?type=1'
    url_img_years = f'{cfg.REQUEST_URL}volume_by_years?type=0'
    url_txt_years = f'{cfg.REQUEST_URL}volume_by_years?type=1'

    # Get quantitive overview image, write it to the 'temp' folder
    img_ov = Image.open(BytesIO(requests.get(url_img_ov).content), formats=['png'])
    img_path_ov = path.join('..', 'temp', 'overview.png')
    img_ov.save(img_path_ov)

    # Get overview text
    text_ov = requests.get(url_txt_ov).text

    # Get volume_by_years image, write it to the 'temp' folder
    img_years = Image.open(
        BytesIO(requests.get(url_img_years).content), formats=['png']
    )
    img_path_years = path.join('..', 'temp', 'volume_by_years.png')
    img_years.save(img_path_years)

    # Get overview text
    text_years = requests.get(url_txt_years).text

    # Send overview image and text to user
    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile(img_path_ov),
        caption=text_ov
    )
    # Send volume_by_years image and text to user
    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile(img_path_years),
        caption=text_years,
        reply_markup=kb.general_keyboard
    )


@dp.message_handler(commands=['correlation_positive', 'correlation_negative'],
                    state=FSMClient.general_state)
async def correlations(message: types.Message):
    '''The handler for correlations stands out as
    caption to the photo is too long to go as one message (> 1024 symb.)'''

    type_of_corr = message.text[12:]

    # Construct URLs to get files from server
    url_img = f'{cfg.REQUEST_URL}correlation{type_of_corr}?type=0'
    url_txt = f'{cfg.REQUEST_URL}correlation{type_of_corr}?type=1'

    # Get necessary image, write it to the 'temp' folder
    img = Image.open(
        BytesIO(requests.get(url_img).content), formats=['png']
    )
    img_path = path.join('..', 'temp', f'correlation{type_of_corr}.png')
    img.save(img_path)

    # Get necessary text
    text = requests.get(url_txt).text

    # Send the image to user
    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile(img_path)
    )
    # Send the text to user
    await bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=kb.general_keyboard
    )


@dp.message_handler(text='Mean price over years', state=FSMClient.general_state)
async def mean_price(message: types.Message):
    with open(path.join('.', 'mean_price_message.txt')) as f:
        m = f.read()
    await message.answer(m, reply_markup=kb.exit_button)
    await FSMClient.years_input.set()


# years_input STATE HANDLERS

@dp.message_handler(regexp='((19[7-9][0-9])|(20[01][0-9])|2020)-((19[7-9][0-9])|(20[01][0-9])|2020)',
                    state=FSMClient.years_input)
async def mean_price(message: types.Message):
    '''Handler for the year range'''

    lowest = message.text[:4]
    highest = message.text[5:]

    url = f'{cfg.REQUEST_URL}mean'
    value = requests.post(url, data={'lowest': lowest, 'highest': highest}).text
    
    await message.answer(
        f'The mean price of all the cars on sale registrated at {lowest}-{highest} is <b>{value}</b> Euros.',
        reply_markup=kb.general_keyboard
    )
    await FSMClient.general_state.set()


@dp.message_handler(text='Exit', state=FSMClient.years_input)
async def mean_price_termination(message: types.Message):
    '''Terminate the years_input state'''

    await message.answer("Ok!", reply_markup=kb.general_keyboard)
    await FSMClient.general_state.set()


@dp.message_handler(state=FSMClient.years_input)
async def mean_price_wrong(message: types.Message):
    '''This handler works, when a user inputs
    neither correct year period nor Exit'''

    with open(path.join('.', 'mean_price_wrong_message.txt')) as f:
        m = f.read()
    await message.answer(m, reply_markup=kb.exit_button)
    # years_input state is still on 
