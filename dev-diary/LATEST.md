# Bootstrap Budget! It’s Been Awhile (Sprint 2)
Well, this is a little embarrassing. My last update on this project was late September 2020. So...yeah...it’s been awhile.

<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/its_been_awhile.png">
</p>

I remember doing a little bit of work in October, but once November hit it was probably downhill from there with holidays and spending some remaining PTO from work. My wife and I also did a lot of work refinishing our hardwood floors (which turned out great BTW) and repainting a large portion of the house.

My actual work also got a little busy from the start of the year by tying up loose ends with projects that had been going on for about a year or more. I started architecting again for other engineers in Bangalore, India and joined a few more extracurricular projects for my team.

I started working on this again throughout the month of June. I rethought how I want Bootstrap to work for me and I feel like I’ve made a ton of progress just with wireframes and some database schema design. I still need to write out the user stories that I’ve been building in my head, but I also didn’t want to start that until I show my progress for this month.

## Cloud vs. Local Install
As I began working on Bootstrap again, I started to rethink its purpose and wanted to focus on a local install instead of cloud since I personally don’t plan to put my data in the cloud long-term. Enabling Bootstrap for the cloud is going to remain a major goal. However, the majority of development for the rest of the year will be done from my local machine at home with the latest version of Node.js installed and using MariaDB and SQLite as my target databases (more on that later). Also, I must admit, the cloud is a scary place.

<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/xkcd_the_cloud.png">
</p>

## Wireframes
The wireframes actually got my mind back in the game with ideas for workflows and the look of the end result. If you remember my very first post when starting Bootstrap, I showed what budgeting looks like for me today: essentially a Google Sheet with a monthly breakdown of certain items summed up based on where my wife and I spent our money.

<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/legacy-budget1.png">
</p>

One reason I’m tired of this is that you don’t really see how many other things like entertainment or subscription fees play into the overall budget, since it’s usually summed up under one of the credit cards. While I could break down the credit cards to a more granular level, it’s not usually clear what my credit card payments actually paid for within the month. There might still be some things charged one month at the end, but were paid for in the next month. Regardless, I still really like this way of looking at my budget. I Especially like the way I can just “project” or plan for some future months to spend a certain amount, type it in the sheet, and see how that affects the year. I knew I wanted to keep this same view, but needed to create a better way to break down and observe budget items. This is where I started sketching the first view of where I wanted to end up. Behold: the dashboard!

<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/bootstrap-user-dashboard-v1.png">
</p>

In the end, this is ultimately what I want to see when I login — An upfront view of the budget year. Through the process of defining a budget, budget items, and accounts with transactions, I should be able to easily track spending and create an actual, defined budget. It all starts with defining said budget.

<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/bootstrap-budgets-v1.png">
</p>

The budget itself is the root of the workflow. In the current state, I generally track budgets year by year, January through December. And defining that fiscal year’s budget is a basic concept that everything else is built on. From here, I can define budget items.

<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/bootstrap-budget-items-v1.png">
</p>

“Budget items” will be my normalized categories that are applied to each of the transactions uploaded for tracking. Here I can define them with a name, a description, a budgeted amount, and a priority. The name and descriptions speak for themselves, but the amount will act as the baseline to indicate if I have gone over budget (displaying red in the dashboard) and act as the projection for future months. The priority sequence controls the order that I would like them to display in the dashboard. For simplicity, I am going to allow for duplicate priorities, but will sort alphabetically as a secondary order format when they are the same. After I have my budget items I can define the accounts where transactions take place.

<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/bootstrap-accounts-v1.png">
</p>

In most budgeting applications I’ve used, the accounts (checking, savings, etc) are the focal point to the data model. For Bootstrap they will be very minor and more of a portal to track each transaction (debit and credit) that will be tied to a budget item. As a secondary purpose, I can also use them to track the current or estimated balance for each. I don’t intend to rely on this too much since I usually spend a lot of time looking at my accounts from their actual websites. Lastly, let's talk about user support.

<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/bootstrap-login-v1.png">
</p>

Although it isn’t a primary focus now, I do intend to have some basic amount of user security baked into Bootstrap since I would consider most of this sensitive data. I also wanted to include a level of budget sharing between users. For example, my wife and I will have individual accounts, yet both of us could see the same budget while creating individual ones for ourselves for different purposes (however unlikely that might be for right now). User accounts, security, and the ability to create and share budgets with other users will start off very small and likely get more advanced in version two.

  
Each of these wireframes were made using diagrams.net (or draw.io) from Google. I personally wouldn’t recommend it, but I don’t feel like buying Visio (my favorite diagramming tool) or using many of the other wireframing services online for right now. It got the job done, although sometimes painstakingly. Not all wireframes are completed yet as some might notice that there is a “Report” section to the nav bar. This will be developed in the next sprint.

## Database and Schema
As the basic wireframes were coming into picture in my head and on the screen, I kept getting distracted with the need to map it all out into a database schema. This is probably where most of my time was spent this month and made it harder to give this update because of the desire to nail down a solid first take.

For the database itself, since I was moving away from the cloud and focusing on a more localized install process, I started looking into SQLite as a start. It made sense to me that a lot of users might not want to install something as large as MySQL or MariaDB, so I wondered if I could keep it all small in scale with SQLite. Later I ended up biting the bullet and installing MariaDB on my personal machine and developing using that too. For now, both will be supported starting with SQLite, but might get dropped later since I might want to focus on just one relational model.

The tables themselves had a large impact on the wireframes when it came to making the budget the focus since I needed a way to abstract many of these concepts in order to share them across users. Below is a diagram of the current schema model and a breakdown of each table.

<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/bootstrap-data-model-v1.png">
</p>

|Table Name|Notes|
|--|--|
|ACCOUNT|Contains all accounts under a given budget. Includes attributes specific to most banking accounts but can be used for other accounts where money flows such as credit cards.|
|BUDGET|References the root budgets that makeup all budget items, accounts and their transactions. Budgets are considered yearly events.|
|BUDGET_ITEM|A breakdown of individual categories for budgeting. This includes a name, budget amount, and priority sequence for viewing in the dashboard.|
|CONFIG|A basic table to contain configurations per user. Although there are no configurations outlined for individual users, there will be admin level configurations for Bootstrap Budget configured and saved at setup.|
|DASHBOARD|Represents the current state of each budget item for each year and month. Called directly for viewing in the dashboard view.|
|TRANSACTION|Contains all transactions (Credit or Debit) logged under a given account and assigned a budget item for calculation on the dashboard. This could also be seen as the “check book”.|
|USER|Holds all user information including basic name, username, password hash, and address information. Will be referenced on most tables as the creator or last user to update a row in many cases.|
|USER_BUDGET|Relates one or many users to a given budget with permissions for what that user can do on the account.|

I don’t doubt that more tables will be needed or that these will need significant updates as the project progresses, but I feel confident that this is the best possible starting point that should allow me to start initial development for CRUD services.

## Setup and Installation Beginnings
Another thing that would distract me was the desire to actually develop something. Earlier in the month I wanted to think more about how installation should go and the groundwork needed to create the tables and set up an initial “ADMIN” user and password system.

For now I’ve settled on using some procedural JavaScript that will also run in Node.js to keep with the full picture. And so far it works well with SQLite. The latest plan is to have a json file for the initial configuration of the database, database location, and address of the API services running locally or externally. This will probably be the first place I start or continue development before I move to creating the actual services.

## Bootstrap Logo Art
Lastly, as ashamed as I am to admit it, for the time I did spend working on this last October, I wasted a lot of it working on some logos for Bootstrap. It’s probably not something to be ashamed of, but I’m very doubtful it was something worth focusing on when I didn’t even have a lot of solid ideas or a single wireframe.

I tried to make something in draw.io first, but it just looked awful. I immediately started looking for a website that made log design easier.

<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/bootstrap-logo-v1.png">
</p>

I ended up finding [LogoMaker](https://logomakr.com/) and that had plenty of searchable clip art to work with and create something free with a limited resolution. I ended up spending about $50 for four download credits. In hindsight it wasn’t really worth the trouble, but it satiated my desire to see what I could create on my own. I think I came up with a decent large and small version that I might use later.

*Large Logo*
<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/bootstrap-logo-v2.png">
</p>

*Small Logo*
<p align="center">
<img src="https://github.com/forgineer/bootstrap-budget/blob/master/dev-diary/images/bootstrap-logo-mini-v2.png">

If this project does take a more serious turn in the future I’ll probably contract someone online to create a better set of logos and other art that could go into the views themselves.

## Next Sprint: Complete User Stories, Wireframes, and Begin Writing Basic Table Services
In the next update, I hope to have the user stories in my head typed out. This should include the overall requirements for a complete install, initial user creation, budget setup, and functionality between each view. As I outline each workflow, they should be accompanied by a view that I haven’t covered above. And if I don’t discern any more table modifications from that, then I’ll get started with writing some basic services to create, read, update, and delete on the tables.

Here’s hoping that the next entry doesn’t take more than a month this time.

*Credit: Melinda Phillips as editor*