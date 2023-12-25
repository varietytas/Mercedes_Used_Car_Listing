from aiogram import executor
import logging
import os
import client # By importing client we run it: create objects, register handlers.


if __name__ == "__main__":
    # Ensure src is the working directory to construct accurate relative paths
    os.chdir(
        os.path.dirname(
            os.path.realpath(__file__)
        )
    )

    logging.basicConfig(
        filename=os.path.join('..', 'logs', 'bot.log'),
        format='%(levelname)s %(threadName)s %(name)s: %(message)s\n',
        level=logging.INFO
    )

    executor.start_polling(client.dp)
