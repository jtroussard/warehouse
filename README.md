# Warehouse Management System
Warehouse Group 2: Samantha Miller, Jacques Troussard, Taylor Dohmen

## Section 1: Introduction

### 1.1 Purpose

The purpose of this document is to describe and provide a detailed plan for the
the warehouse management system project in Computer Science (CPSC)-430.  The
audience of this document includes the writers&#39; professor Dr. Karen Anewalt
and BGCVA&#39;s representative, Gusty Cooper.

### 1.2 Scope

The scope of this project to is provide a software application that manages
automobile inventory for a primary and mobile warehouses, including sales and
invoices.  Cooper represents the primary stakeholder in this project.  The
project will upload, display, and search products that BGCVA sells.  This
application intends to improve organization and track business statistics for
the stakeholders.

### 1.3 Document Conventions

The document follows this terminology:

-  &quot;**SHALL**&quot; indicates a hard requirement that **SHALL** be
implemented.

-  &quot;**SHOULD**&quot; indicates a soft requirement that may be
implemented if time allows.

### 1.4 Document Overview

This document is organized as follows:

- Section 2 provides a general description of the system, including its
  overview, user characteristics, functional requirements, and constraints.
- Section 3 contains the project&#39;s schedule, including the approach,
  milestones deliverables, work breakdown structure, Gannt chart, and task
dependency diagram.
- Appendix A contains a glossary of commonly used terms.
- Appendix B provides examples and explanations of project documents.
- Appendix C enumerates the document contributions by each member in the group.

## Section 2: Project Description

### 2.1 Project Scope

The warehouse management system will be an application by which BGCVA employees
can manage inventory and sales records. It will digitally store information
about each warehouse, the products in each warehouse, sales that have taken
place, and the employees. Through the system, employees will be able to query
product and sales data, generate sales reports and invoices, and update
inventory. Inventory updates will consist of operations related to transferring
items between warehouses, inputting newly ordered items into the system, and
selling items to customers. All databases will be hosted on a server in the
cloud, and will be accessible via a browser interface. Only employees will be
able to access the system, and will need to login with a unique username and
password to take advantage of system functions.

### 2.2 User Characteristics

This web application interfaces with the clients as an internal tool to track
products, sales, and employee metrics. There should be administrators who
interface with the system to provide technical support, but have no need to
engage with the product, unless other users need help. They may be able to
update product fields and perform site maintenance as needed. They should have
access to every feature on the site for testing, explanation, and future
improvement. There are warehouse managers who should also have full site access,
except for administrator pages, for training and business information, including
managing products and employees as well as their metrics. The clients include
sales associates who move product and make sales using their mobile warehouse
vans to local customers. Sales associates should not have access to the user
accounts and metrics portions of the site. Administrators, managers, and sales
associates should be able to access the &quot;working&quot; parts of the site,
including searching for products, creating and displaying invoices, and
importing product files to update the system. Customers are local automobile
repair and supply shops who buy the products the sales associates offer.
Customers and the general public may not login or create accounts to use the
application because it remains an tool internal to the business and its
associates.

### 2.3 Functional Requirements

_2.3.1. Log into System_

_Description:_ A user accessing the site has a email and password to use the
application.

_Main Flow:_

1. User accesses site by Internet browser.
2. System displays login screen, prompting email and password fields, and a
Login button.
3. User types email and password and clicks Login.
4. System verifies matching user information and displays the Home page of the
site.

_Alternate Flow A:_

1. User accesses site page that requires login, like the Home or Import page.
2. The system redirects any user without a session to the Login page.

_Alternate Flow B:_

3. The user types either the email or password.  The Login button is disabled
until both fields are filled.

_Alternate Flow C:_

3. The user types a wrong email or password.

4. The system checks the provided information and returns a error message
proclaiming the email or password was invalid.

5. Repeat until Main Flow 4 is met.

_2.3.2. Log out of System_

_Description:_ A logged-in user exits the site.

_Main flow:_

1. A logged-in user clicks the Logout button on the menu.
2. The system removes the user from the session and displays the Login page of
the application.

_2.3.3. Search for Product_

_Description:_ Any user can search for products based on warehouse location,
product name, or product number.

_Main Flow:_

1. A logged-in user navigates to the Search page via the menu bar.
2. The system displays the Search page, which offers options to search for
products by warehouse location, product name, or product number, as well as
Search and Reset buttons.
3. The user enters requirements in the form and clicks Search.
4. The system queries all related information and displays all product
information in the table.

_Alternate Flow A:_

3. The user clicks the Reset button instead of Search.

4. The system clears the fields of the search boxes.

_Alternate Flow B:_

5. The user clicks the Reset button after searching.

6. The system clears the returned table and search fields.

_Import Inventory File_

_Description_: Any user should be able to upload a CSV file into the system
which specifies what changes are being made to the warehouse inventory. The
system should then update the product database to account for the specified
changes.

_Main Flow_:

1. User navigates to an inventory management page and selects the option to
upload an inventory management file.
2. System displays an upload window including a file explorer and upload button.
3. User navigates the file explorer, selects the desired file, and clicks the
upload button.
4. The system parses the file and updates the inventory database based on the
file&#39;s specification. If the operation is time intensive, the system should
display a progress indicator to the user.
5. The system displays a message informing the user that the operation was
executed successfully.

_Alternate Flow A_:

1. The system parses the file and finds that it is improperly formatted.
2. The System displays a message informing the user that the file is improperly
formatted. Return to Main Flow 1.

_Alternate Flow B_:

1. The system parses the file and finds that there is an invalid operation.
2. The System displays a message informing the user of bad operation. Return to
Main Flow 1.

_Create Invoice_

_Description_: A sales associate should be able to select a subset of their
mobile warehouse&#39;s inventory and create and invoice for the sale of those
items.

_Main Flow_:

1. Sales associate navigates to a Create Invoice page.
2. System displays form with a field for entering customer information, a list
of the products in the sales associate&#39;s mobile warehouse with areas to
specify the sold quantity of each item, and a submit button.
3. Sales associate enters the customer&#39;s information, specifies the quantity
of each item being sold, and selects submit.
4. System validates that the quantities are not larger than the quantity of the
item in stock.
5. System generates invoice based on the price and quantities of the items sold
and customer information given and saves the sale record in the database.
6. System updates inventory database to account for the sold items.
7. System displays message indicating that the sale was successfully documented.

_Alternate Flow A_:

1. System finds that a sale quantity is larger than the inventory quantity and
displays a message indicating this. Return to Main Flow 2.

_Search for Invoice (by Sales Associate, Customer, Date)_

_Description_: Any user should be able to search for and review records of
previous sales.

_Main Flow_:

1. User navigates to sales page.
2. System displays a list of previous sales, sorted by date (most recent first),
a search field, a drop-down menu to select search field, and a search button .
3. User selects what field they want to search by, enters a term into the search
field, and selects search.
4. System queries the sales database to and displays a list of sales records
that match the search terms.
5. User selects a particular search result.
6. System displays invoice and an option to download the invoice as a txt file
for that particular sale.

_Generate Sales Metrics (by associate between range of dates)_

_Description_: A manager should be able to generate a report detailing what each
sales associate sold, given a date range.

_Main Flow_:

1. Manager navigates to sales metrics page.
2. System displays input fields for start date and end date and a generate
report button.
3. Manager fills in the date fields and selects generate report.
4. System queries the sales database and compiles how many of each item each
associate sold during the time period.
5. System displays a list of associates, each with a sublist of items the
quantity of each that the associate sold.

Create a User Account

Description: The administrator should be able to create any user accounts and
the inventory manager should be able to create sale associate accounts, allowing
unique sales associates to access their inventory stores.

_Main Flow(Admin):_

1. Administrator log into the postgres database as root user.
2. Administrator creates an inventory manager role with a preselected list of
privileges allowing them to access and modify the &#39;users&#39; table as well
as all other tables necessary to facilitate the manager&#39;s functions.

_Main Flow(Manager):_

1. Manager logs into their account.
2. System compares credentials to SQL users table
3. Manager navigates to manage users management page
4. System queries users database and renders a table with users and check boxes
5. Manager selects &#39;Create User&#39;
6. System renders web form containing all the necessary fields required to
insert a new user.
7. Manager finishes form and selects submit (reset simply clears form)
8. System receives post request from manager user, scrubs input and updates SQL
users table.
9. System generates password and renders success page with username and password

_Alternate Flow:_

9.   System generates non-generic error and renders error page

Update a User Account

Description: The inventory manager should be able to update the various
attributes associated with any a user account of lesser privilege level.

1. Manager logs into their account
2. System compares credentials to SQL user tables
3. Manager navigates to user page
4. System queries users database and renders a table with users and check boxes
5. Manager selects user checkbox and clicks Update user
6. System queries database for user and attributes
7. System renders a web form preloaded with user attributes.
8. System logs date, time, manager id, and user&#39;s details
9. Manager refills desired user attribute fields and selects Submit
10. System receives post request from manager user, scrubs input and updates SQL
users table and appends changes to log
11. System generates success page.

_Alternate Flow:_

10. System generates non-generic error and renders error page

Disable a User Account

Description: The inventory manager **SHOULD** be able to modify the access status to
the system of any user account of lesser privilege level.

1. Manager logs into their account
2. System compares credentials to SQL user tables
3. Manager navigates to user page
4. System queries users database and and renders a table with users and check
boxes
5. Manager selects user checkbox and clicks Update user
6. System queries database for user and attributes
7. System renders a web form preloaded with user attributes.
8. System logs date, time, manager id, and user&#39;s details.
9. Manager toggles Disable/Enable radio button and selects submit.
10. System receives post request from manager user, scrubs input and updates SQL
users table and appends changes to log.
11. System generates success page.

_Alternate Flow:_

10. System generates non-generic error and renders error page

Update Product Attributes

Description: Inventory manage should be able to access list of products queried
from database and modify attributes individually.

_Main Flow:_

1. Manager logs into their account
2. System compares credentials to SQL user tables
3. Manager navigates to inventory management page
4. System renders management page with link to modify item
5. Manager click modify item link
6. System renders page with part description field and submit button
7. Manager enters item key terms (part number, name, etc.)
8. System queries database and renders table with possible matches
9. Manager selects item and clicks on Modify
10. System renders item page, a preloaded web form with item attributes.
11. Manager modifies data and clicks submit
12. System receives post request from manager user, scrubs input and updates SQL
users table and appends changes to log.

_Alternate Flow:_

12. System generates non-generic error and renders error page

### 2.4 Constraints

Performance, security, hardware, software, etc

## Section 3: Project Schedule

### 3.1 Approach

The development team has constructed the project schedule by subdividing the requirements into milestones and deliverables.  These divisions of smallest shippable code can be packaged to the production environment and presented to the stakeholders for testing and feedback.  Once development and production environments have been established, the developers may begin working on the Product Import functionality and Search features.  Since these features will be the most used, and other facets of the site require their functionality, their completion should come first.  Then, there will be time for subsequent feedback, while other parts of the application are built.
<br>
Once the developers have created the core importing and searching functionalities, they may begin dependent tasks, including invoice generation and user account and session functionality for the application.  After these milestones have been delivered, the medium priority requirements are available, such as Customer Management and Metrics pages.  Once medium priority requirements have been addressed, the lowest priorities, including Invoice Search and more complex user account support may be implemented.

### 3.2 Milestones and Deliverables

Initialize Dev and Production environments

Define Database Schema

Create the Import Page - 1 week

- --Create file template to be read.
- --Create web page to process and display results.
- --Create python script to read and validate input.
- --Create python script to perform database operations.

Create the Search Page - 3 days

- --Create web page to search for and display results.
- --Create python script to read and validate input.
- --Create python script to perform database operations.

Create Invoice Page - 3 days

- --Create web page to process and display results.
- --Create python script to read and validate input.
- --Create python script to perform database operations.
- --Create downloadable text file.

Basic User Accounts - 2 days

- --Implement user roles for session management in Python.
- --Login and logout functionality.
- --Create account generation for Administrator roles.

Create Customer Management page - 2 days

- --Create web page to create and update customers.
- --Create python script to read and validate input.
- --Create python script to perform database operations.

Metrics - 3 days

- --Create web page to search for and display results.
- --Create python script to read and validate input.
- --Create python script to perform database operations.

Search for Invoice Page - 3 days

- --Create web page to search for and display results.
- --Create python script to read and validate input.
- --Create python script to perform database operations.

Advanced User Accounts - 2 days

- --Update warehouse information.
- --Update user information.

### 3.3 Work Breakdown Structure

### 3.4 Gannt Chart -taylor

### 3.5 Task Dependency Diagram -taylor

## Appendix A. Glossary

This appendix contains a list of abbreviations used in this document.

## Appendix B. System Documents

B.1 Product Import

The table below lists the columns and data types associated with a product
import, which updates the quantities and locations tracked in the system.

| **Field** | **Data Type** | **Notes** |
| --- | --- | --- |
| From Warehouse | Integer | Should match a unique system number identifying the
warehouse.
If entering the main warehouse as new stock, this value is 0. |
| To Warehouse | Integer | Should match a unique system number identifying the
warehouse. |
| Product Number | Integer | If new, this value is 0.
If updating, number matches the product number in the system. |
| Quantity | Integer | The amount of product being moved from one warehouse to
another. |
| Price | Double | The price per unit.  This field is read only if the product
is new stock entering the main warehouse (From Warehouse value of 0.) |
| Description | String | The description of the product.  This field is read
only if the product is new stock entering the main warehouse (From Warehouse
value of 0.) |

B.2 Invoice Example

Below captures the text file created from the system when a sale is made.

Business Name

123 Example Dr.

Ashland, VA 23005

&lt;phone number&gt;

&lt;email&gt;

To:

Business Name

123 Example Dr.

Ashland, VA 23005

Cc. Manager Name

&lt;BG Distributive Group Company Name&gt; Invoice

Invoice Number: ##

Date: mm-dd-yyyy

Product Name                        Qty        Price                Product
Number                Total Amount

Test 1    1 $56.00  10100    $56.00

Test 2    3 $15.00  16534    $45.00

Total           $101

## Appendix C. Document Contributions

This appendix lists each group member&#39;s document contributions.

- Samantha Miller
  - Wrote the Section 1: Introduction.
  - Wrote Section 2.2 User Characteristics and requirements  2.3.1 through
    2.3.3.
  - Created System Documents B.1 and B.2.
  
- Jacques Troussard
  - Wrote requirements 2.3.7 through 2.3.10
  - Wrote Section 2.4 Constraints
  - Created work breakdown graph



