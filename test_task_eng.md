
# **Test Task for Junior Python Developer Position**

## **1. API**   
### **Description**   
The task is to implement an API for storing user links.

### User Requirements   
- The user should be able to register (email, password)   
- The user should be able to change their password   
- The user should be able to reset their password   
- The user should be able to authenticate   
- The user should be able to manage their links (create, edit, delete, view)

- The user should be able to manage their collections (create, edit, delete, view)

### Functional Requirements   
#### Links   
A link should include the following fields:   
- Page title   
- Short description   
- Page URL   
- Image   
- Link type (website, book, article, music, video). If the page type cannot be determined, default to "website". The preview image should be taken from the "og:image" field.   
- Creation date and time   
- Modification date and time   

When adding a link, the user only provides the URL. The service retrieves the remaining data automatically. The information can be found in the Open Graph metadata within the HTML code of the page. You need to load the page code and extract the relevant data. Open Graph metadata may not always be present; in such cases, extract information from the "title" and "meta description" tags if available. Learn more about Open Graph here: [https://yandex.com/support/webmaster/open-graph/intro-open-graph.html](https://yandex.com/support/webmaster/open-graph/intro-open-graph.html) or use any other information source.   
*Links can be grouped into collections. The same link can belong to multiple collections. Links should be unique for each user.*   

#### Collections   
Collections should include the following fields:   
- Name (required)   
- Short description (optional)   
- Creation date and time   
- Modification date and time   

### **Non-functional Requirements**   
- Python 3.12+   
- Django 5.0+ (Django Rest Framework)   
- API documentation using Swagger   
- Use Docker (candidates who do not use Docker will not be considered)   
- Provide a startup guide in README.md   

Additional Benefits:   
- Project deployment   

P.S. You can use any libraries or Django add-ons as needed.   

## **2. SQL**   
**Description**   
*Write an SQL query* that returns the top 10 users with the highest number of saved links. If multiple users have the same number of links, prioritize those who registered earlier.

You may write a script or use external libraries to populate the database with test data.
