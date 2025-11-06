# 🔄 Loopify - Automate API Calls

**"Upload a CSV, grab a coffee, and watch your APIs do the work for you!"**

## 🚀 What's Loopify?

Loopify is your new best friend for testing APIs. Tired of clicking "Send" over and over? We get it! Loopify lets you upload a CSV file with all your API requests and runs them automatically. It's like having a tiny robot that tests APIs while you focus on more important things (like that coffee ☕).

### Our Superpower 🦸
**CSV-Powered Batch Testing** - The feature that'll make you wonder how you lived without it:
- Upload a CSV with all your API requests
- Set it and forget it - runs automatically
- Perfect for testing workflows, webhooks, or just bulk operations
- Add delays between requests to be nice to servers

## ✨ What Can Loopify Do?

### 🔧 Single Request Mode
- **All the HTTP Methods**: GET, POST, PUT, DELETE, PATCH - we speak them all
- **cURL Importer**: Got a cURL command? Paste it and we'll handle the rest
- **Smart Body Types**: JSON, Form Data, or Raw Text - whatever your API craves
- **Headers Galore**: Add as many headers as you want (even that weird custom one)
- **Pretty Responses**: We format JSON responses so they're actually readable

### 🚀 LOOPIFY PRO (The Main Event!)
**Batch processing made stupidly simple:**
- 📁 **CSV/JSON Upload**: Drag, drop, done
- ⏱️ **Configurable Delays**: Don't overwhelm servers (unless you want to 😈)
- 📊 **Results Dashboard**: See all your responses in one pretty table
- 💾 **Export Results**: Download everything as CSV for your records
- 🎯 **Sample Templates**: Not sure about the format? We've got examples!

## 🎯 Why You'll Love Loopify

### For the Busy Developer 🏃
"Testing 20 endpoints used to take me 15 minutes. Now it takes 15 seconds. I've literally gained back hours of my life."

### For the Forgetful Tester 🐠
"Never again will I forget to test that one obscure endpoint. Loopify remembers everything for me."

### For the Lazy Genius 😴
"Why click 'Send' 50 times when I can click 'Upload' once? It's just basic math."


## 📋 How to Use the Batch Magic

### Step 1: Prepare Your CSV
Create a CSV that looks like this:

| method | url | headers | payload_type | payload |
|--------|-----|---------|--------------|---------|
| GET | https://api.example.com/users | `{"Authorization": "Bearer token"}` | none | |
| POST | https://api.example.com/users | `{"Content-Type": "application/json"}` | json | `{"name": "John", "email": "john@example.com"}` |
| PUT | https://api.example.com/users/1 | `{"Content-Type": "application/json"}` | json | `{"name": "John Updated"}` |

### Step 2: Upload & Relax
1. Go to the "🚀 LOOPIFY PRO" tab
2. Upload your CSV file
3. Set how long to wait between requests
4. Hit "Run Batch"
5. Go get that coffee ☕

### Step 3: Profit! 💰
Watch as Loopify runs all your requests and shows you the results in a beautiful table. Download the results if you need to show your boss how productive you've been.

## 🎨 Cool Features You Might Miss

### The Little Things That Matter
- **Pretty UI**: We made it not ugly (you're welcome)
- **cURL Import**: Steal API calls from your terminal with pride
- **Response History**: Remember what you did last time
- **Error Handling**: We tell you what went wrong in plain English
- **No Overwhelming Options**: Clean, simple, gets the job done

## 🤔 Who's This For?

### Perfect For:
- 👨‍💻 **Backend Developers** testing their APIs
- 🧪 **QA Engineers** running test suites
- 🔗 **Webhook Testing** for multiple events
- 📊 **Data Engineers** hitting multiple endpoints
- 🎓 **Students** learning about APIs
- 😴 **Anyone who hates repetitive clicking**

### Probably Not For:
- 🧙‍♂️ Wizards who can test APIs with their mind
- 🤖 Robots (you're probably already automated)
- 🐌 People who enjoy doing things the slow way

## 🐛 Found a Bug? Have an Idea?

We're human! (Mostly) Found something broken? Have a feature that would make your life easier? 

[Open an issue](https://github.com/Ramc26/loopify/issues) or even better - fork it and make it better! We love pull requests almost as much as we love coffee.

## 👨‍💻 Author

**Thought...Designed and Developed by Ram Bikkina** 🦉 [ramc26.github.io/RamTechSuite](https://ramc26.github.io/RamTechSuite)

For suggestions, fun banter, or freelancing opportunities, feel free to reach out:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/rambikkina26/)
[![Email](https://img.shields.io/badge/Email-Contact%20Me-red?logo=gmail)](mailto:itsrambikkina@gmail.com)

---

**Crafted with care by 🦉 [RamTechSuite](https://ramc26.github.io/RamTechSuite) | Hosted on Streamlit**