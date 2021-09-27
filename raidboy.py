# Import
import random
import time
import json
from itertools import cycle
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest


def init():
    # Storage
    tgs = []
    hype = []

    # Settings
    delayBetweenRaid = 15 
    delayAfterStart = 3
    delayAfterHype = 1
    delayBetweenCount = 0.5
    countdownFrom = 5
    randomHypePercentage = 100
    startMsg = "🔥🔥ALLRIGHT GUYS IM YOUR RAID LEADER, LISTEN UP. DO YOU WANT TO PUMP YOUR BAG? LETS GOOOOOO🔥🔥"

    # Read config.json
    json_file =  open('config.json', 'r')
    json_data = json.loads(json_file.read())
    api_id = json_data['api_id']
    api_hash = json_data['api_hash']
    session_name = json_data['session_name']
    json_file.close()

    # Connection with telephon
    client = TelegramClient(session_name, api_id, api_hash)

    # Ask if we should start the program
    def askStart():
        check = str(input("\nShould we start raiding in "+ channel +" ? (Y/N): \n")).lower().strip()
        try:
            if check[0] == 'y':
                with client:
                    client.loop.run_until_complete(start())
            elif check[0] == 'n':
                quit()
            else:
                print('Invalid Input')
                return askStart()
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return askStart()


    # Read our telegram.txt file and put them in tgs[]
    # We use .rstrip() to slice /n from the string (which means new line)
    def readTgs():
        with open("/lists/telegram.txt", encoding="utf8") as file:
            for line in file:
                tgs.append(line.rstrip())

    # Read our randomhype.txt and put them in hype[]
    def readHype():
        with open("/lists/randomhype.txt", encoding="utf8") as file:
            for line in file:
                hype.append(line.rstrip())        

    # Return a random hype message from the hype[]
    # If its empty we fill it again!
    def randomHype():
        # Refill the list if its empty
        if not hype:
            readHype()
        # Select a random index from the list
        index = random.randrange((len(hype)))
        # Get the string at this index
        string = hype[index]
        # remove it from the list so we dont get duplicates
        hype.pop(index)
        # Return the string
        return string

    # Check if we should send out a hype message
    def shouldHype():
        return random.randrange(100) < randomHypePercentage

    # Start the fucking bot bro just fuckin start it already
    async def start():
        print("\n----------------PoC----------------------")
        print("Joining channel " + channel)

        # Storage
        started = False

        # fill our lists
        readTgs()
        readHype()

        # We want to start the list again when we reach the end
        # we use a cycle for that
        tg_cyle = cycle(tgs)    

        # Join the TG channel
        await client(JoinChannelRequest(channel))
        print(channel + " joined! Starting ... ")

        # loop the TG list infinitly
        # Meaning we can only stop it with ctrl+c for now.
        while True:
            # Next channel in cycle
            tg = next(tg_cyle)

            # Is this the first telegram we are raiding?
            if not started:
                await client.send_message(channel, startMsg)
                print(startMsg)
                time.sleep(delayAfterStart)
            else: 
                # Delay between raids
                time.sleep(delayBetweenRaid)

            # Should we do a hype message? If so, fucking send it mate.
            # Dont do this if we didn't start yet
            if started and shouldHype():
                hypeMsg = randomHype()
                await client.send_message(channel, hypeMsg,)
                print(hypeMsg)
                time.sleep(delayAfterHype)

            # Do the count down with a delay
            count = countdownFrom
            while count > 0:
                countString = str(count)
                await client.send_message(channel, countString )
                print(countString)
                count -= 1
                time.sleep(delayBetweenCount)

            # Send the fucking TG 
            await client.send_message(channel, tg)
            print(tg)   


            # We started this raid so we have to change this.
            if not started:
                started = True

    # Start script
    # Get user input and prompt for a start
    channel = input("What channel do you want to post to?\n")
    askStart()

init()
