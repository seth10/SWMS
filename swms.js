const Discord = require('discord.js');
const client = new Discord.Client();
const token_login = require('swms-token');
const schedule = require('node-schedule');

client.on('ready', () => {
    let message = 'SWMS Discord chatbot ready!';
    console.log(message);
    client.channels.find('name', 'bot').send(message);
});

client.on('message', message => {
    if (message.author.username != client.user.username)
        console.log('message from ' + message.author.username);
    if (message.content === 'ping')
        message.reply('pong');
});

const morning_messages = [
    'Good morning! On a scale of 1-10, how much energy do you have?',
];
//const morning_notification = schedule.scheduleJob('0 9 * * 1-5', () => {
const morning_notification = schedule.scheduleJob('1 * * * *', () => {
    let message = morning_messages[Math.floor(Math.random()*morning_messages.length)];
    client.channels.find('name', 'bot').send(message);
});

token_login(client);
