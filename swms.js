const Discord = require('discord.js');
const client = new Discord.Client();
const token_login = require('swms-token');
const schedule = require('node-schedule');

const morning_messages = [
    'Good morning! On a scale of 1-10, how much energy do you have?'
];

function getGratitudeMessage(userID) {
    const gratitude_messages = [
        `Thank you for your response, <@${userID}> :smiley:`
    ]
    return gratitude_messages[Math.floor(Math.random()*gratitude_messages.length)];
}

client.on('ready', () => {
    let message = 'SWMS Discord chatbot ready!';
    console.log(message);
});

client.on('message', message => {
    if (message.author.username != client.user.username) {
        message.channel.startTyping();
        function respond() { 
            message.author.send(getGratitudeMessage(message.author.id));
            message.channel.stopTyping();
        }
        client.setTimeout(respond, 2000);
    }
});

const morning_notification = schedule.scheduleJob('0 9 * * 1-5', () => {
    let message = morning_messages[Math.floor(Math.random()*morning_messages.length)];
    client.users.find('username', 'Seth').send(message);
});

token_login(client);
