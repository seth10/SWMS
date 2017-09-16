const Discord = require('discord.js');
const client = new Discord.Client();
const token_login = require('swms-token');

client.on('ready', () => {
    console.log('I am ready!');
});

client.on('message', message => {
    console.log("message from " + message.author.username);
    if (message.content === 'ping') {
        message.reply('pong');
    }
});

token_login(client);
