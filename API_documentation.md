# API documentation
myenv\scripts\activate
python manage.py runserver

## Auth API 

----------------------------------------------------------------
    GET
    /auth/email-verify/ - auth_email-verify_list

----------------------------------------------------------------
    POST
    /auth/login/ - auth_login_create

----------------------------------------------------------------
    POST
    /auth/register/ - auth_register_create


## Stores API


----------------------------------------------------------------
    GET
    /stores/ - stores_list

----------------------------------------------------------------
    POST
    /stores/ - stores_create

----------------------------------------------------------------
    GET
    /stores/{id} - stores_read

----------------------------------------------------------------
    PUT
    /stores/{id} - stores_update

----------------------------------------------------------------
    PATCH
    /stores/{id} - stores_partial_update

----------------------------------------------------------------
    DELETE 
    /stores/{id} - stores_delete
### Staffs
### Products

## StoreAdmin