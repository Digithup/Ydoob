'use strict';
(function() {
    var db = {
        loadData: function(filter) {
            return $.grep(this.clients, function(client) {
                return (!filter.Name || client.Name.indexOf(filter.Name) > -1)
                    && (!filter.Action || client.Action === filter.Action)
                    && (!filter.ProductsCategory || client.ProductsCategory.indexOf(filter.ProductsCategory) > -1)
                    && (!filter.ProductsubCategory || client.ProductsubCategory === filter.ProductsubCategory)
                    && (filter.Married === undefined || client.Married === filter.Married);
            });
        },
        insertItem: function(insertingClient) {
            this.clients.push(insertingClient);
        },
        updateItem: function(updatingClient) { },

        deleteItem: function(deletingClient) {
            var clientIndex = $.inArray(deletingClient, this.clients);
            this.clients.splice(clientIndex, 1);
        }
    };
    window.db = db;
    db.countries = [
        { Name: "India", Id: 0 },
        { Name: "United States", Id: 1 },
        { Name: "Canada", Id: 2 },
        { Name: "United Kingdom", Id: 3 },
        { Name: "France", Id: 4 },
        { Name: "Brazil", Id: 5 },
        { Name: "China", Id: 6 },
        { Name: "Russia", Id: 7 }
    ];
    db.clients = [
        {
            "User Key": "user:usersaaa.user-lists",
            "Russian" : "список пользователей",
            "Arabic": ".قوائم المستخدمين",
            "English": "user lists",
        },
        {
            "User Key": "user:usersaaa.user-first-name",
            "Russian" : "имя пользователя",
            "Arabic": "اسم المستخدم الأول",
            "English": "user first name",
        },
        {
            "User Key": "user:usersaaa.user-last-name",
            "Russian" : "фамилия пользователя",
            "Arabic": "اسم المستخدم الأخير",
            "English": "user last name",
        },
        {
            "User Key": "user:usersaaa.user-login",
            "Russian" : "логин пользователя",
            "Arabic": "دخول المستخدم",
            "English": "user login",
        },
        {
            "User Key": "user:usersaaa.user-add-catalog",
            "Russian" : "добавить продукт",
            "Arabic": "أضف المنتج",
            "English": "add catalog",
        },
        {
            "User Key": "user:usersaaa.user-orders-list",
            "Russian" : "упорядоченный список",
            "Arabic": "قائمة الأوامر",
            "English": "orders list",
        },
        {
            "User Key": "user:usersaaa.user-coupon-list",
            "Russian" : "список купонов",
            "Arabic": "قائمة القسائم",
            "English": "coupon list",
        },
        {
            "User Key": "user:usersaaa.user-new-password",
            "Russian" : "пользователя новый пароль",
            "Arabic": ".مستخدم جديد كلمة مرور",
            "English": "user new password",
        },
        {
            "User Key": "user:usersaaa.user-reset-password",
            "Russian" : "сброс пароля",
            "Arabic": "أعد ضبط كلمة السر",
            "English": "user reset password",
        },
        {
            "User Key": "user:usersaaa.user-email-id",
            "Russian" : "идентификатор электронной почты",
            "Arabic": "هوية البريد الإلكتروني",
            "English": "email id",
        },
        {
            "User Key": "user:usersaaa.user-roles",
            "Russian" : "роль пользователя",
            "Arabic": "أدوار المستخدم",
            "English": "user roles",
        },
        {
            "User Key": "user:usersaaa.user-profile-information",
            "Russian" : "информация профиля",
            "Arabic": "معلومات التوصيف",
            "English": "profile information",
        },
        {
            "User Key": "admin:admin.button.delete",
            "Russian" : "удалить",
            "Arabic": "احذف",
            "English": "delete",
        },
        {
            "User Key": "admin:admin.button.save",
            "Russian" : "спасать",
            "Arabic": "احفظ",
            "English": "save",
        },
        {
            "User Key": "admin:admin.button.edit",
            "Russian" : "редактировать",
            "Arabic": "حرر",
            "English": "edit",
        },
        {
            "User Key": "admin:admin.tabs.general",
            "Russian" : "главные вкладки",
            "Arabic": "الألسنة العامة",
            "English": "general tabs",
        },
        {
            "User Key": "category:categories.physical",
            "Russian" : "физический",
            "Arabic": "جسدي",
            "English": "physical",
        },
        {
            "User Key": "category:categories.digital",
            "Russian" : "цифровой",
            "Arabic": "رقمي",
            "English": "digital",
        },
        {
            "User Key": "category:categories.sub.category",
            "Russian" : "промежуточная категория",
            "Arabic": "الفئة الفرعيةر",
            "English": "sub category",
        },
        {
            "User Key": "media:media.dropzone",
            "Russian" : "зона сброса",
            "Arabic": "منطقة الإسقاط",
            "English": "dropzone",
        },
        {
            "User Key": "vendor:vendors.vendor-lists",
            "Russian" : "списки поставщиков",
            "Arabic": "قوائم البائعين",
            "English": "vendor lists",
        },
        {
            "User Key": "vendor:vendors.vendor-first-name",
            "Russian" : "имя поставщика",
            "Arabic": "اسم البائع الأول",
            "English": "vendor first name",
        },
        {
            "User Key": "vendor:vendors.vendor-last-name",
            "Russian" : "фамилия поставщика",
            "Arabic": "اسم عائلة البائع",
            "English": "vendor last name",
        },
        {
            "User Key": "vendor:vendors.vendor-login",
            "Russian" : "вход поставщика",
            "Arabic": "تسجيل دخول البائعين",
            "English": "vendor login",
        },
        {
            "User Key": "vendor:vendors.vendor-add-catalog",
            "Russian" : "добавить продукт",
            "Arabic": "أضف المنتج",
            "English": "add catalog",
        },
        {
            "User Key": "vendor:vendors.vendor-orders-list",
            "Russian" : "упорядоченный список",
            "Arabic": "قائمة الأوامر",
            "English": "orders list",
        },
        {
            "User Key": "user:usersaaa.user-coupon-list",
            "Russian" : "список купонов",
            "Arabic": "قائمة القسائم",
            "English": "coupon list",
        },
        {
            "User Key": "vendor:vendors.vendor-new-password",
            "Russian" : "новый пароль поставщика",
            "Arabic": "كلمة مرور جديدة للبائع",
            "English": "vendor new password",
        },
        {
            "User Key": "vendor:vendors.vendor-reset-password",
            "Russian" : "пароль сброса поставщика",
            "Arabic": "إعادة تعيين كلمة السر للبائع",
            "English": "vendor reset password",
        },
        {
            "User Key": "vendor:vendors.vendor-email-id",
            "Russian" : "идентификатор электронной почты",
            "Arabic": "هوية البريد الإلكتروني",
            "English": "email id",
        },
        {
            "User Key": "vendor:vendors.vendor-roles",
            "Russian" : "роли поставщиков",
            "Arabic": "باء-أدوار البائعين",
            "English": "vendor roles",
        },
        {
            "User Key": "vendor:vendors.vendor-profile-information",
            "Russian" : "информация профиля",
            "Arabic": "معلومات التوصيف",
            "English": "profile information",
        },
        {
            "User Key": "admin:admin.tabs.general",
            "Russian" : "главные вкладки",
            "Arabic": "الألسنة العامة",
            "English": "general tabs",
        },
        {
            "User Key": "media:media.dropzone",
            "Russian" : "зона сброса",
            "Arabic": "منطقة الإسقاط",
            "English": "dropzone",
        },
        {
            "User Key": "category:categories.digital",
            "Russian" : "цифровой",
            "Arabic": "رقمي",
            "English": "digital",
        },
        {
            "User Key": "category:categories.sub.category",
            "Russian" : "промежуточная категория",
            "Arabic": "الفئة الفرعيةر",
            "English": "sub category",
        },
        {
            "User Key": "category:categories.physical",
            "Russian" : "физический",
            "Arabic": "جسدي",
            "English": "physical",
        }
    ];
    db.users = [
        {
            "ID": "x",
            "Account": "A758A693-0302-03D1-AE53-EEFE22855556",
            "Products Title": "Carson Kelley",
            "RegisterDate": "2002-04-20T22:55:52-07:00"
        },
        {
            "Account": "D89FF524-1233-0CE7-C9E1-56EFF017A321",
            "Products Title": "Prescott Griffin",
            "RegisterDate": "2011-02-22T05:59:55-08:00"
        },
        {
            "Account": "06FAAD9A-5114-08F6-D60C-961B2528B4F0",
            "Products Title": "Amir Saunders",
            "RegisterDate": "2014-08-13T09:17:49-07:00"
        },
        {
            "Account": "EED7653D-7DD9-A722-64A8-36A55ECDBE77",
            "Products Title": "Derek Thornton",
            "RegisterDate": "2012-02-27T01:31:07-08:00"
        },
        {
            "Account": "2A2E6D40-FEBD-C643-A751-9AB4CAF1E2F6",
            "Products Title": "Fletcher Romero",
            "RegisterDate": "2010-06-25T15:49:54-07:00"
        },
        {
            "Account": "3978F8FA-DFF0-DA0E-0A5D-EB9D281A3286",
            "Products Title": "Thaddeus Stein",
            "RegisterDate": "2013-11-10T07:29:41-08:00"
        },
        {
            "Account": "658DBF5A-176E-569A-9273-74FB5F69FA42",
            "Products Title": "Nash Knapp",
            "RegisterDate": "2005-06-24T09:11:19-07:00"
        },
        {
            "Account": "76D2EE4B-7A73-1212-F6F2-957EF8C1F907",
            "Products Title": "Quamar Vega",
            "RegisterDate": "2011-04-13T20:06:29-07:00"
        },
        {
            "Account": "00E46809-A595-CE82-C5B4-D1CAEB7E3E58",
            "Products Title": "Philip Galloway",
            "RegisterDate": "2008-08-21T18:59:38-07:00"
        },
        {
            "Account": "C196781C-DDCC-AF83-DDC2-CA3E851A47A0",
            "Products Title": "Mason French",
            "RegisterDate": "2000-11-15T00:38:37-08:00"
        },
        {
            "Account": "5911F201-818A-B393-5888-13157CE0D63F",
            "Products Title": "Ross Cortez",
            "RegisterDate": "2010-05-27T17:35:32-07:00"
        },
        {
            "Account": "B8BB78F9-E1A1-A956-086F-E12B6FE168B6",
            "Products Title": "Logan King",
            "RegisterDate": "2003-07-08T16:58:06-07:00"
        },
        {
            "Account": "06F636C3-9599-1A2D-5FD5-86B24ADDE626",
            "Products Title": "Cedric Leblanc",
            "RegisterDate": "2011-06-30T14:30:10-07:00"
        },
        {
            "Account": "FE880CDD-F6E7-75CB-743C-64C6DE192412",
            "Products Title": "Simon Sullivan",
            "RegisterDate": "2013-06-11T16:35:07-07:00"
        },
        {
            "Account": "BBEDD673-E2C1-4872-A5D3-C4EBD4BE0A12",
            "Products Title": "Jamal West",
            "RegisterDate": "2001-03-16T20:18:29-08:00"
        },
        {
            "Account": "19BC22FA-C52E-0CC6-9552-10365C755FAC",
            "Products Title": "Hector Morales",
            "RegisterDate": "2012-11-01T01:56:34-07:00"
        },
        {
            "Account": "A8292214-2C13-5989-3419-6B83DD637D6C",
            "Products Title": "Herrod Hart",
            "RegisterDate": "2008-03-13T19:21:04-07:00"
        },
        {
            "Account": "0285564B-F447-0E7F-EAA1-7FB8F9C453C8",
            "Products Title": "Clark Maxwell",
            "RegisterDate": "2004-08-05T08:22:24-07:00"
        },
        {
            "Account": "EA78F076-4F6E-4228-268C-1F51272498AE",
            "Products Title": "Reuben Walter",
            "RegisterDate": "2011-01-23T01:55:59-08:00"
        },
        {
            "Account": "6A88C194-EA21-426F-4FE2-F2AE33F51793",
            "Products Title": "Ira Ingram",
            "RegisterDate": "2008-08-15T05:57:46-07:00"
        },
        {
            "Account": "4275E873-439C-AD26-56B3-8715E336508E",
            "Products Title": "Damian Morrow",
            "RegisterDate": "2015-09-13T01:50:55-07:00"
        },
        {
            "Account": "A0D733C4-9070-B8D6-4387-D44F0BA515BE",
            "Products Title": "Macon Farrell",
            "RegisterDate": "2011-03-14T05:41:40-07:00"
        },
        {
            "Account": "B3683DE8-C2FA-7CA0-A8A6-8FA7E954F90A",
            "Products Title": "Joel Galloway",
            "RegisterDate": "2003-02-03T04:19:01-08:00"
        },
        {
            "Account": "01D95A8E-91BC-2050-F5D0-4437AAFFD11F",
            "Products Title": "Rigel Horton",
            "RegisterDate": "2015-06-20T11:53:11-07:00"
        },
        {
            "Account": "F0D12CC0-31AC-A82E-FD73-EEEFDBD21A36",
            "Products Title": "Sylvester Gaines",
            "RegisterDate": "2004-03-12T09:57:13-08:00"
        },
        {
            "Account": "874FCC49-9A61-71BC-2F4E-2CE88348AD7B",
            "Products Title": "Abbot Mckay",
            "RegisterDate": "2008-12-26T20:42:57-08:00"
        },
        {
            "Account": "B8DA1912-20A0-FB6E-0031-5F88FD63EF90",
            "Products Title": "Solomon Green",
            "RegisterDate": "2013-09-04T01:44:47-07:00"
        }
     ];
}());
