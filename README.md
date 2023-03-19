## Speech-to-Text-discord-Bot
A pycord based script to do speech to text using speech_recognition module

## Using
Add your bot `token` on line 76

```python
bot.run("TOKEN")
```

And then just run main.py
```bash
$python3 main.py
```
To start Recording use `,start` cmd and `,stop` once done
![image](https://user-images.githubusercontent.com/75514601/226164041-aee3507f-00a7-4583-96f9-b64f66080102.png)

To record individual user_audios in `.mp3` format, uncomment line 21

```python
await channel.send(f"finished recording audio for: {', '.join(recorded_users)}.", files=files)  # Send a message with the accumulated files.
```
![image](https://user-images.githubusercontent.com/75514601/226164557-88c54a0e-ee55-40bb-9705-84f4279761e3.png)

Works even if two users say different things at the same time in the same vc
![image](https://user-images.githubusercontent.com/75514601/226164625-dfd24d95-16f8-4675-ad98-c9100d09e94f.png)


## Thoughts
- Live transcript in this usecase has not been possible due to the way `start_recording` in pycord has been implemented 
- It could work if you modify the source sink class a bit but that's out of scope for this as I wrote this sort of as a quick hack script for my main role-playing discord bot.
- You could migrate from using `,start` and `,stop` to events like muting and unmuting mic for a smoother experience
- DM **Adrick#6640** 
