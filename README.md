# Data Extractor Script

This is a custom python script that scrapes out data from JSON files that I found while pentesting a web application.

The JSON file has the data in the format as given below:

{
	"list":{
		"is_banned_comment":false,
		"user_id":133445069,
		"nickname":"Erik",
		"head_url":"sadfahagaas.jpg",
		"nationality":"TRY",
		"is_turn_on_mic":true,
		"role":1
		}
}

With a bunch of other details.

But I just wanted these information to be extracted in a different file.

So this script basically scrapes out these data from the provided file and spits out the infos in another file.

----------------------------------------
Nickname: Erik
User ID: 56546516546
Nationality: TRY
Head URL: sadfahagaas.jpg
----------------------------------------


