import discord
import requests
from bs4 import BeautifulSoup
import math
from godAbbreviations import godAbbreviations

with open('token.txt', 'r') as file:
  token = file.readline()


def createItemBuildEmbed(godName, itemString):
    embedVar = discord.Embed(color=0x7fffd4)
    #print("https://static.smite.guru/i/champions/icons/{}.jpg".format(godName))
    embedVar.set_thumbnail(url="https://static.smite.guru/i/champions/icons/{}.jpg".format(godName))
    embedVar.set_author(name=godName, url="https://smite.guru/builds/{}".format(godName), icon_url="https://static.smite.guru/i/champions/icons/{}.jpg".format(godName))
    embedVar.add_field(name="Here are the 6 most popular items for {}".format(godName), value=itemString, inline=True)
    return embedVar


def createGuidedBuildEmbed(godName, itemList, percentageList):
    embedVar = discord.Embed(color=0x7fffd4)
    starterList = [itemList[0], itemList[1], itemList[2]]
    bootsList = [itemList[3], itemList[4], itemList[5]]
    relicList = [itemList[6], itemList[7], itemList[8], itemList[9]]
    coreItemsList = [itemList[10], itemList[11], itemList[12], itemList[13]]
    starterPercentageList = [percentageList[0], percentageList[1], percentageList[2]]
    bootsPercentageList = [percentageList[3], percentageList[4], percentageList[5]]
    relicPercentageList = [percentageList[6], percentageList[7], percentageList[8], percentageList[9]]
    coreItemsPercentageList = [percentageList[10], percentageList[11], percentageList[12], percentageList[13]]
    for index in range(len(relicList) - 1, -1, -1):
        if relicList[index] == "Vision Shard":
            relicList.pop(index)
            relicPercentageList.pop(index)
    print(starterList)
    print(bootsList)
    print(relicList)
    print(coreItemsList)
    print(starterPercentageList)
    print(bootsPercentageList)
    print(relicPercentageList)
    print(coreItemsPercentageList)
    embedVar.set_thumbnail(url="https://static.smite.guru/i/champions/icons/{}.jpg".format(godName))
    embedVar.set_author(name=godName, url="https://smite.guru/builds/{}".format(godName), icon_url="https://static.smite.guru/i/champions/icons/{}.jpg".format(godName))
    embedVar.add_field(name="Popular Blessings", value=starterList[0] + ": " + starterPercentageList[0] + "\n"
                       + starterList[1] + ": " + starterPercentageList[1] + "\n"
                       + starterList[2] + ": " + starterPercentageList[2],
                       inline=True)
    embedVar.add_field(name="Popular Boots", value=bootsList[0] + ": " + bootsPercentageList[0] + "\n"
                       + bootsList[1] + ": " + bootsPercentageList[1] + "\n"
                       + bootsList[2] + ": " + bootsPercentageList[2],
                       inline=True)
    embedVar.add_field(name="Popular Relics", value=relicList[0] + ": " + relicPercentageList[0] + "\n"
                       + relicList[1] + ": " + relicPercentageList[1] + "\n"
                       + relicList[2] + ": " + relicPercentageList[2],
                       inline=False)
    embedVar.add_field(name="Popular Core Items", value=coreItemsList[0] + ": " + coreItemsPercentageList[0] + "\n"
                       + coreItemsList[1] + ": " + coreItemsPercentageList[1] + "\n"
                       + coreItemsList[2] + ": " + coreItemsPercentageList[2] + "\n"
                       + coreItemsList[3] + ": " + coreItemsPercentageList[3],
                       inline=True)
    return embedVar


def mathStuff(equation):
    finalValue = 0
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


def pull_build_data(godName):
    site_url = "http://smite.guru"
    site_dir = "/builds/" + godName
    site_html = requests.get(site_url + site_dir).text
    soup = BeautifulSoup(site_html, "html.parser")

    # itemList = []
    # for item in soup.select(".primary-item img"):
    #     itemList.append(item["alt"])
    # return itemList

    # for string in soup.find_all("span"):
    #     print(soup.span.string)

    itemsAndPercentagesLists = []
    itemList = []
    percentageList = []
    spanList = soup.select("span")
    for number in range(44, 58):
        percentageList.append(spanList[number].string)
    print(percentageList)
    print(len(percentageList))
    #print(spanList[44].string)
    for item in soup.select(".item.item-row__img img"):
        itemList.append(item["alt"])
    print(itemList)
    print(len(itemList))
    itemsAndPercentagesLists.append(itemList)
    itemsAndPercentagesLists.append(percentageList)
    return itemsAndPercentagesLists


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
        if message.author == client.user:
            return

        if message.content.startswith("$saymyname"):
            await message.channel.send(message.author)

        if message.content.startswith("dab"):
            await message.channel.send(":Dab:")

        if message.content.startswith("$hello"):
            await message.channel.send("Hello friends")

        if message.content.startswith("$math"):
            equation = message.content.split()
            equation.pop(0)
            await message.channel.send(mathStuff(equation))

        if message.content.startswith('$test'):
            embedVar = discord.Embed(color=0x7fffd4)
            #embedVar.set_thumbnail(url="https://static.smite.guru/i/champions/icons/eset.jpg")
            embedVar.set_author(name="Eset", url="https://smite.guru/builds/eset", icon_url="https://static.smite.guru/i/champions/icons/eset.jpg")
            # embedVar.set_image(url="https://static.scientificamerican.com/sciam/cache/file/41DF7DA0-EE58-4259-AA815A390FB37C55_source.jpg")
            # embedVar.set_image(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/132.png")
            embedVar.add_field(name="Build", value="<:veryaveragedab:828016535708237875>", inline=True)
            await message.channel.send(embed=embedVar)

        if message.content.startswith("$build"):
            messageContent = message.content.split()
            messageContent.pop(0)
            print(messageContent)
            if len(messageContent) > 1:
                unformattedGodName = ""
                for part in messageContent:
                    unformattedGodName = unformattedGodName + part + " "
                unformattedGodName.strip()
                print(unformattedGodName)
                godName = godAbbreviations(unformattedGodName)
            else:
                godName = godAbbreviations(messageContent[0])
            print(godName)
            itemList = pull_build_data(godName)[0]
            percentageList = pull_build_data(godName)[1]
            itemString = ""
            for item in itemList:
                if item == itemList[0]:
                    itemString = itemString + item
                else:
                    itemString = itemString + ", " + item
            if itemString == "":
                await message.channel.send("Not a god lol")
            else:
                itemBuildEmbed = createGuidedBuildEmbed(godName, itemList, percentageList)
                await message.channel.send(embed=itemBuildEmbed)

        if message.content.startswith("$ban"):
            await message.channel.send("Priveledges have been revoked from Bean Bean #5753")


    client.run(token)
