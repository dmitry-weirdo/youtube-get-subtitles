scp -i /c/_wiki-bot/ec2-wiki-bot-keypair.pem \
  ./dist/youtube-subtitles-bot.pyz \
  ec2-user@ec2-3-75-96-233.eu-central-1.compute.amazonaws.com:/home/ec2-user/youtube-subtitles-bot/youtube-subtitles-bot.pyz
