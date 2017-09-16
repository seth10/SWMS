const Discord = require('discord.js');
const client = new Discord.Client();
const auth_token = require('swms.token');

client.on('ready', () => {
    console.log('I am ready!');
});

client.on('message', message => {
    console.log("message from " + message.author.username);
    if (message.content === 'ping') {
        message.reply('pong');
    }
});

auth_token(client);
