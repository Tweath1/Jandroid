import discord
import requests
from bs4 import BeautifulSoup
from godFunctions import godAbbreviations

with open('token.txt', 'r') as file:
    token = file.readline()


def split_by_char(string):
  charList = []
  for char in string:
    charList.append(char)
  return charList


def createItemBuildEmbed(godName, itemString):
    prettyGodName = ""
    prettyGodNameList = godName.split("-")
    for index in range(len(prettyGodNameList)):
        prettyGodNameList[index] = prettyGodNameList[index].capitalize()
    for item in prettyGodNameList:
        prettyGodName = prettyGodName + item + " "
    embedVar = discord.Embed(color=0x7fffd4)
    embedVar.set_thumbnail(url="https://static.smite.guru/i/champions/icons/{}.jpg".format(godName))
    embedVar.set_author(name=prettyGodName, url="https://smite.guru/builds/{}".format(godName), icon_url="https://static.smite.guru/i/champions/icons/{}.jpg".format(godName))
    embedVar.add_field(name="Here are the 6 most popular items for {}".format(godName), value=itemString, inline=True)
    return embedVar


def createGuidedBuildEmbed(godName, itemList, percentageList):
    prettyGodName = ""
    prettyGodNameList = godName.split("-")
    for index in range(len(prettyGodNameList)):
        prettyGodNameList[index] = prettyGodNameList[index].capitalize()
    for item in prettyGodNameList:
        prettyGodName = prettyGodName + item + " "
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

    embedVar.set_thumbnail(url="https://static.smite.guru/i/champions/icons/{}.jpg".format(godName))
    embedVar.set_author(name=prettyGodName, url="https://smite.guru/builds/{}".format(godName), icon_url="https://static.smite.guru/i/champions/icons/{}.jpg".format(godName))
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
                       inline=True)
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

def pull_build(godName):
    site_url = "http://smite.guru"
    site_dir = "/builds/" + godName
    site_html = requests.get(site_url + site_dir).text
    soup = BeautifulSoup(site_html, "html.parser")

    itemList = []
    for item in soup.select(".primary-item img"):
        itemList.append(item["alt"])
    return itemList

def pull_build_data(godName):
    site_url = "http://smite.guru"
    site_dir = "/builds/" + godName
    site_html = requests.get(site_url + site_dir).text
    soup = BeautifulSoup(site_html, "html.parser")

    itemsAndPercentagesLists = []
    itemList = []
    percentageList = []
    spanList = soup.select("span")
    mark = 0
    startingNum = 0
    newList = []
    splitStringLists = []
    for item in spanList:
        newList.append(split_by_char(item))
    for thing in newList:
        splitStringLists.append(split_by_char(thing[0]))
    for thing1 in range(len(splitStringLists)):
        for thing2 in splitStringLists[thing1]:
            if thing2 == '%' and mark == 0:
                mark += 1
                startingNum = thing1
    for number in range(startingNum+30, startingNum+44):
        percentageList.append(spanList[number].string)
    for item in soup.select(".item.item-row__img img"):
        itemList.append(item["alt"])
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

        if message.content.startswith("$hello"):
            await message.channel.send("Hello friends")

        if message.content.startswith("$math"):
            equation = message.content.split()
            equation.pop(0)
            await message.channel.send(mathStuff(equation))

        if message.content.startswith("$items"):
            messageContent = message.content.split()
            messageContent.pop(0)
            if len(messageContent) > 1:
                unformattedGodName = ""
                for part in messageContent:
                    unformattedGodName = unformattedGodName + part + " "
                unformattedGodName = unformattedGodName.strip()
                godName = godAbbreviations(unformattedGodName)
            else:
                godName = godAbbreviations(messageContent[0])
            infoList = pull_build_data(godName)
            itemList = infoList[0]
            percentageList = infoList[1]
            if itemList == []:
                await message.channel.send("Not a god lol")
            else:
                guidedBuildEmbed = createGuidedBuildEmbed(godName, itemList, percentageList)
                await message.channel.send(embed=guidedBuildEmbed)

        if message.content.startswith("$cc"):
            messageContent = message.content.split()
            messageContent.pop(0)
            if len(messageContent) > 1:
                unformattedGodName = ""
                for part in messageContent:
                    unformattedGodName = unformattedGodName + part + " "
                unformattedGodName = unformattedGodName.strip()
                godName = godAbbreviations(unformattedGodName)
            else:
                godName = godAbbreviations(messageContent[0])
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
                itemBuildEmbed = createItemBuildEmbed(godName, itemString)
                await message.channel.send(embed=itemBuildEmbed)


#test
    client.run(token)
