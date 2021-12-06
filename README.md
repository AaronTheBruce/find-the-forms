# Versions
Python v3.9.7
geckodriver v0.30.0-linux32.tar.gz unpacked to ./venv/bin

# Steps to Setup
- clone or extract to the location of your choice. Desktop will do for demonstrative purposes.
- Setup your venv and source into it, I created it within the root of this app
- Add geckodriver to your ./venv/bin/ (I did this while developing for Firefox before I switched to Chrome in the end. Add it if it breaks without)
- pip install -r requirements.txt

I ended up going to webdriver.Chrome() instead since Firefox was a pain to configure.

# Usage

### Prompt
I have a basic prompt for the user to select F for searching and D for downloading. It's not elegant, but it helps me decide which actions to take since there are only 2.

The user will be prompted when searching / option 'F' to keep entering Form names until the user hits 'y'/'Y' to stop the prompting. 

I entered 'Form W-2', 'Form W-2P', and 'Publ 1'. W-2P is incorrect so it does not result in any output. Form W-2 and Publ 1 both get assessed and printed out to the console.

### Listing out json for the existing Filenames and their starting and ending years

![anim](https://user-images.githubusercontent.com/56603706/144771183-6564bf28-74b1-4ab3-b0e6-51c77a493be5.gif)

### Downloading PDFs by Filename and a starting year and an ending year

The user will be prompted for only 1 Form name, a starting year, and an ending year. Then the app gets to work as shown below.

![anim](https://user-images.githubusercontent.com/56603706/144770895-a6aff409-dc63-4167-a965-cb21e3cb3ebc.gif)


### Nice to haves

I'd like to refactor the code to be DRYer. There is a bit of repetition between the 2 primary function that I don't like. I'd like to make more use of the services folder where applicable. I tried to make use of it for some simpler repeatable logic.

Also right now the search only prints the json to the console. I think it'd be better if it was downloaded as well. But, I already took a good amount of time working on this. So, I think it is okay for now.
