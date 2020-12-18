import face_recognition
import urllib.request
import urllib.error
import os
import discord
import asyncio


def is_known_face(url):
    request = urllib.request.Request(url, data=None, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'
    })

    response = urllib.request.urlopen(request)

    unknown_face = face_recognition.load_image_file(response)
    unknown_encoding = face_recognition.face_encodings(unknown_face)[0]

    return True in face_recognition.compare_faces(known_encodings, unknown_encoding)


def get_known_encodings():
    for filename in os.listdir(KNOWN_FACES_DIR):
        known_face = face_recognition.load_image_file(KNOWN_FACES_DIR + '/' + filename)
        known_encodings.append(face_recognition.face_encodings(known_face)[0])


def start_discord_bot():
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user.name}#{client.user.discriminator}')

        activity = discord.Activity(type=discord.ActivityType.watching, name='your every move')
        await client.change_presence(activity=activity)

    @client.event
    async def on_message(message):
        image_file_extensions = ('png', 'jpg', 'jpeg')
        not_allowed = False

        for attachment in message.attachments:
            if attachment.url.endswith(image_file_extensions) and is_known_face(attachment.url):
                not_allowed = not_allowed or True

        for embed in message.embeds:
            if embed.type == 'image' and is_known_face(embed.url):
                not_allowed = not_allowed or True

        if not_allowed:
            await message.delete()
            sent_message = await message.channel\
                .send(f'<@{message.author.id}> This image is not allowed on this server!')

            await asyncio.sleep(10)
            await sent_message.delete()

    client.run(DISCORD_TOKEN)


def has_embedded_image(message):
    for embed in message.embeds:
        if embed.type == 'image':
            return True

    return False


if __name__ == '__main__':
    KNOWN_FACES_DIR = 'images'
    DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

    known_encodings = []
    get_known_encodings()

    start_discord_bot()
