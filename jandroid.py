import discord
import requests
from bs4 import BeautifulSoup

with open('token.txt', 'r') as file:
  thing = file.readline()


def split_by_char(string):
    charList = []
    for char in string:
        charList.append(char)
    return charList


def math(equation):
    num1 = float(equation[0])
    num2 = float(equation[2])
    operator = equation[1]

    if operator == "+":
        finalValue = num1 + num2
    if operator == "-":
        finalValue = num1 - num2
    if operator == "*" or operator == "x":
        finalValue = num1 * num2
    if operator == "/":
        finalValue = num1 / num2

    return finalValue


def pull_build(godName):
    site_url = "http://smite.guru"
    site_dir = "/builds/" + godName[0]
    site_html = requests.get(site_url + site_dir).text
    soup = BeautifulSoup(site_html, "html.parser")

    # print("For {}, the following items are most popular".format(godName[0]))

    itemList = []
    for item in soup.select(".primary-item img"):
        itemList.append(item["alt"])
    return itemList


if __name__ == '__main__':
    print("hello world")

    client = discord.Client()


    @client.event
    async def on_connect():
        print("We have connected as {0.user}".format(client))


    @client.event
    async def on_ready():
        print("We have logged in as {0.user}".format(client))


    @client.event
    async def on_message(message):
        if message.content.startswith("$saymyname"):
            await message.channel.send(message.author)

        if message.author == client.user:
            return

        if message.content.startswith("$hello"):
            await message.channel.send("Hello friends")

        if message.content.startswith("$math"):
            equation = message.content.split()
            equation.pop(0)
            await message.channel.send(math(equation))

        if message.content.startswith("$build"):
            godName = message.content.split()
            godName.pop(0)
            itemList = pull_build(godName)
            itemString = ""
            for item in itemList:
                if item == itemList[0]:
                    itemString = itemString + item
                else:
                    itemString = itemString + ", " + item
            if itemString == "":
                await message.channel.send("Not a god lol")
            else:
                await message.channel.send(itemString)

        if message.content.startswith("$ban"):
            await message.channel.send("Priveledges have been revoked from Bean Bean #5753")


    client.run("ODI2NDcyMTM2Njg3NzQ3MTMy.YGM-KA.ksiz7wi6yGxJpfd24x6YkRn_mSY")
