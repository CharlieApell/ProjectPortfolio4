# The Simple Man Spirits - Testing 

[Main README.md file](/README.md)

[View live project](https://pp4-capell.herokuapp.com/)

[View GitHub repository](https://github.com/CharlieApell/ProjectPortfolio4)

***
## Table of contents
1. [Testing User Stories](#Testing-User-Stories)
2. [Manual Testing](#Manual-Testing)
3. [Automated Testing](#Automated-Testing) 
     - [Code Validation](#Code-Validation)
     - [Browser Validation](#Browser-Validation)
4. [User Testing](#User-Testing)


***

## Testing User Stories

#### User Stories:
1. As a **Site User** I can **view a paginated list of recipes** so that **I can select one to read**.
  
    - The list of recipes on the home page has been paginated by 21. If there are more than 21 recipes, the remainder moves to the next page. This will continue until there are 21 or less recipe cards on the one page.

2. As a **Site User** I can **click on a recipe** so that **I can read the full text**.
    
    - On each recipe card, there is a concise summary of the recipe along with a clickable button that directs the user to the recipe page. There, they can access a comprehensive list of ingredients and the step-by-step method how to make the cocktail.

3. As a **Site User / Admin** I can **view the number of likes on each recipe** so that **I can see which is the most popular or viral**.

    - The recipe cards display the total number of likes received for each recipe, and this information is also visible on the recipe page itself.

4. As a **Site User / Admin** I can **view comments on an individual recipe** so that **I can read the conversation**.

    - A comments section has been incorporated into the recipe pages, displaying the author's username and the date/time when the comment was posted.

5. As a **Site User** I can **register an account** so that **I can comment and like recipes**.

    - The website provides a sign-in and sign-up option, which prompts users on the home page to log in for accessing certain content. Users are required to be signed in to access protected features, such as liking and commenting. Additionally, users have the option to log in using their Google account.

6. As a **Site User** I can **leave comments on a recipe** so that **I can be involved in the conversation**.

    - A comment section has been incorporated into the recipe pages for users to comment on the recipes.

7. As a **Site User** I can **like or unlike a recipe** so that **I can interact with the content**.

    - If the user is logged in, they can like or unlike a recipe.

8. As a **Site User** I can **search for recipes** so that **I find the recipe I'm looking for**.

    - A search field to search for cocktails has been implemented at the top to make it easier to find what you are looking for.

9. As a **Site Admin** I can **create, read, update and delete recipes** so that **I can manage my content**.

    - As a Site Admin, I have the ability to create, read, update, and delete recipes, enabling me to effectively manage my content..

10. As a **Site Admin** I can **create draft recipes** so that **I can finish writing the recipes later**.

    - As a Site Admin, I have the capability to create draft recipes, allowing me to save unfinished recipes for completion at a later time.

11. As a **Site User** I can **delete my account** so that **if I no longer want to be a member I don't have to**.

    - When a user is logged in, they will be able to delete their account.

12. As a **Site User** I can **share the content** so that **I can post it on my Facebook Page**.

    - If a user wants, they can easily share the recipe to their Facebook Page.

13. As a **Site User** I can **edit or delete my own comment** so that **I can manage my content**.

    - When a user is logged in and they are the author of a comment, they will see two buttons on the Recipe Detail page. By clicking the blue 'Edit' button, they will be directed to the Edit Comment page, where they can make changes to their comment and resubmit it to the site. 
    By clicking the red "Delete" button will delete the user's comment.

14. As a **Site Admin** I can **edit or delete comments directly on the recipe page** so that **I don't have to do it through the Admin Page**.

    - As a Site Admin, I have the ability to edit or delete comments directly on the recipe page using two buttons: a blue 'Edit' button and a red 'Delete' button. This enables me to manage comments conveniently without the need to navigate to the Admin Page.

15. As a **Site User** I can **like or unlike a comment** so that **I can interact with the content**.

    - When a user is logged in they can like or unlike a comment. (still in progress)

[Back to top](#The-Simple-Man-Spirits---Testing)

## Manual Testing

### Common Elements Testing
Manual testing was performed on the following elements present on each page:

- Test the functionality of the Logo by ensuring it redirects to the home screen.

- Test the navigation links to verify they are working correctly.

- Test the social links to confirm they open in a new page as expected.

### Home Page
Manual testing was conducted on the following elements of the [Home Page](https://pp4-capell.herokuapp.com/):
     
- Test that user welcome message displays username.

    - On logging in, there is a message alert at the top of the Home page which tells the user that they have successfully logged in.
    - Further down the Home page, there is a message which welcomes the user (by name) back to the site.

- Test that recipe cards redirect user to recipe pages.

    - The headline, excerpt and image of each recipe card redirects the user to the Recipe Detail page for the recipe they have clicked on.

### Recipe Page
Manual testing was conducted on the following elements of the [Recipe Pages](https://pp4-capell.herokuapp.com/)
     
- Test that recipes can be liked and unliked when logged in.
     
- Test that comments can be submitted.

- Test that comments can be edited by author and admin/superuser only.

- Test that comments can only be deleted by author and admin/superuser only.

- Test that a success message is given when a user deletes or edits a commment.

### Share Recipe Page
Manual testing was conducted on the following elements of the [Add Recipe Page](https://pp4-capell.herokuapp.com/):

- Test that recipes create unique slugs, based on the title of the recipe.

- Test that recipes with the same title will throw an error and ask the user to rename the recipe to something unique.

- Test that recipes with an unrealistic prep or cook time will throw an error.
     
- Test that recipes are saved.
     
### Sign in/Sign Out/Sign Up Pages
Manual testing was conducted on the following elements of the [Sign In Page](https://pp4-capell.herokuapp.com/accounts/login/), [Sign Out Page](https://pp4-capell.herokuapp.com/accounts/logout/), [Sign Up Page](https://pp4-capell.herokuapp.com/accounts/signup/) and [Delete Account Page](https://pp4-capell.herokuapp.com/delete-account/)

- Users can register, log in, logout and delete account.

### Pages are Responsive
- Manual testing was conducted for responsiveness on large, medium and small screens.

[Back to top](#The-Simple-Man-Spirits---Testing)

## Automated Testing

### Code Validation
The [W3C Markup Validator](https://validator.w3.org/ "Link to M£C Markup Validator Site") service was used to validate the `HTML` and `CSS` code used.<br>
The PEP8 Python Validator in GitPod and [CI Python Linter](https://pep8ci.herokuapp.com/) was used to validate the `Python` code used.

**Results:**

- HTML Pages - Code Validation

HTML validation - all pages clear.

- CSS stylesheet - Code Validation

CSS tested clear.

- Python Files - Code Validation

**Files tested**

capellpp4 - urls.py

capellpp4 - settings.py

blog - admin.py

blog - forms.py

blog - models.py

blog - urls.py

blog - views.py

All files tested clear.

### Browser Validation
- Chrome
- Safari
- Firefox

## User testing 
My husband and the lovely people of Slack were asked to review the site and documentation to point out any bugs and/or user experience issues. Their helpful advice throughout the process led to a few small UX changes in order to create a better experience. 

[Back to top](#The-Simple-Man-Spirits---Testing)

***