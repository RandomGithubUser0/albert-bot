from playwright.sync_api import sync_playwright, TimeoutError
import time
import re

# ─── CREDENTIALS ──────────────────────────────────────────────────────────────
EMAIL    = "your@email.com"
PASSWORD = "yourpassword"

# ─── SPEED CONFIG ─────────────────────────────────────────────────────────────
HEADLESS       = False   # False to watch the browser
PAGE_LOAD_WAIT = 0    # seconds to wait after navigating to each URL
BETWEEN_CHECKS = 0    # seconds to pause between URL checks
LOGIN_WAIT     = 2.5    # seconds to wait after submitting login

# ─── URLS TO CHECK ────────────────────────────────────────────────────────────
# Paste your list here — non-URL lines (labels, blank lines) are ignored.
URLS_TEXT = """
Check Point 2:  Algebra 2 Skills Requirement

You are to achieve “ADVANCED PROFICIENCY"  for EACH skill. Each link represents one skill. 

Numerical & Algebraic Expressions
https://www.albert.io/adaptive/skill/c237ed61-bfd0-444e-afcd-c45c48afdb5e 
https://www.albert.io/adaptive/skill/1e8e52d7-67c5-44e6-a443-3310137a576e 

Function Foundations 
https://www.albert.io/adaptive/skill/59b6251e-a0b3-4b62-b2f2-72901975b55e 

https://www.albert.io/adaptive/skill/7cec4739-f437-4a46-a654-85a3be7e846a
https://www.albert.io/adaptive/skill/c66c33e3-307f-4d9e-9e77-ba214975ad41 

https://www.albert.io/adaptive/skill/6018337f-9cb0-4376-96d9-16f284e3797b 
https://www.albert.io/adaptive/skill/7fda4189-b1b4-4c0d-bc83-02dec3c9ec02 
https://www.albert.io/adaptive/skill/61090d73-d065-4347-8116-246bc731def1 

https://www.albert.io/adaptive/skill/bdca27ce-9997-40ea-845f-1933fa1eb3fa 
https://www.albert.io/adaptive/skill/a0875290-6dec-41b8-ae60-1c513895da11 
https://www.albert.io/adaptive/skill/433bea5a-041f-4399-96b5-d072cfc387e8 
https://www.albert.io/adaptive/skill/8b993971-8eff-4ed3-a17b-2bc2948b8386 

https://www.albert.io/adaptive/skill/b568f8f7-f024-4c2d-bf13-14576268aef6 
https://www.albert.io/adaptive/skill/b90a492b-b792-4825-88f4-7c28b7f4c59e 

https://www.albert.io/adaptive/skill/f3399a47-de1a-4aa6-a825-d578ebef7441 
https://www.albert.io/adaptive/skill/4c37781f-77af-406b-8ab8-bf0e367eb93f 
https://www.albert.io/adaptive/skill/cfe4b723-5d17-4988-8f21-74609b2015f2 

https://www.albert.io/adaptive/skill/13585e68-c7ba-485a-a4c0-caca997f5ef6 

https://www.albert.io/adaptive/skill/9ab14a32-110d-43fe-a629-6a037daeea5a 
https://www.albert.io/adaptive/skill/95356190-e483-4f2b-8004-d213724b232c 
https://www.albert.io/adaptive/skill/8a34b30c-e5e0-4955-89e8-ed6802dda7e5 
https://www.albert.io/adaptive/skill/8b61d82e-3aca-4d19-af97-a2c8891b64a1 

Linear Equations & Inequalities
https://www.albert.io/adaptive/skill/c30e9d0f-2a48-4bc6-9282-2efd598eafc5 
https://www.albert.io/adaptive/skill/e1ca92ea-a897-49d3-a0c3-c25e4cca3614 
https://www.albert.io/adaptive/skill/a988665b-148d-4d97-9a92-e3a58d18c959 

https://www.albert.io/adaptive/skill/a26af866-2364-4b91-a8fd-845aecc6947f 
https://www.albert.io/adaptive/skill/30434b27-4c32-45e0-8437-39e297994c17 
https://www.albert.io/adaptive/skill/7dfd437e-25ea-44b6-b25c-cbb09b73c8f9 

Creating & Reasoning with Equations
https://www.albert.io/adaptive/skill/bef3c2d2-3bf8-4003-ada7-67cefc91f2c2 

https://www.albert.io/adaptive/skill/1517006e-03eb-4b6e-b0f2-959cf424aff9 

Linear Functions & Models
https://www.albert.io/adaptive/skill/6953db05-6192-48bb-9f0f-6610d244f67e 
https://www.albert.io/adaptive/skill/ac562848-244e-4144-981b-36f7f1667ffd 

https://www.albert.io/adaptive/skill/ef34501b-6a3d-4695-bc16-f37f3566aa3e 
https://www.albert.io/adaptive/skill/ab4126af-b790-4a75-9473-fa471c7685d4 
https://www.albert.io/adaptive/skill/76b1f948-9aa1-4c8c-a3c9-c7045b147999 

Expressing Geometry with Equations 
https://www.albert.io/adaptive/skill/8cbf4847-da9e-4a5c-946a-c50bb87f7430 
https://www.albert.io/adaptive/skill/609e5ce6-9c31-4639-ba4e-05c6b60f380e 
https://www.albert.io/adaptive/skill/6b11c4a7-2348-41bf-a309-4ab05521b58a 
https://www.albert.io/adaptive/skill/0d45e2d5-230f-4f0a-b6bf-295ab86016fe 

Circles & Coordinate Geometry
https://www.albert.io/adaptive/skill/36457a22-6d04-49ec-9ceb-1b6641c6e038 

Polynomial Expressions & Operations
https://www.albert.io/adaptive/skill/09d94f89-5751-4ff6-90bc-f7beec6be54c 
https://www.albert.io/adaptive/skill/9cdfb5ac-03d9-49b4-9f61-797ef1067e5f 

https://www.albert.io/adaptive/skill/07d91562-918e-4f75-a8be-55c68868ff88 
https://www.albert.io/adaptive/skill/4276786a-e2ce-4b7a-80fe-6859809c5e05 
https://www.albert.io/adaptive/skill/460bbab8-ebfd-49fd-983b-78e9ec8421a3 

https://www.albert.io/adaptive/skill/a67e7004-a316-4b15-a4d3-a95d31f0bc53 
https://www.albert.io/adaptive/skill/a7a96237-e030-4908-a50f-02defa5622e9 
https://www.albert.io/adaptive/skill/2168c391-b2a3-4b44-992c-761b11ecdbfd 
https://www.albert.io/adaptive/skill/67002dd4-0d2f-4bfb-a0ea-cbedeeeda284 

https://www.albert.io/adaptive/skill/bc9def39-8e36-4c28-b799-9ff81ad65f50 
https://www.albert.io/adaptive/skill/c49478e5-2391-4cbc-b819-6963f832fbfa 
https://www.albert.io/adaptive/skill/bbf151ad-1bab-4f71-8ec4-3001b62d8b4b 
https://www.albert.io/adaptive/skill/1a66ec22-4e15-477a-b9fd-fd7484602ce7 
https://www.albert.io/adaptive/skill/4ee6faf8-4499-4d93-8d70-77985e0f050d 

https://www.albert.io/adaptive/skill/8e7819ad-4b29-4dce-8e9a-0a6f39771fc6 
https://www.albert.io/adaptive/skill/1659865d-dad9-4c04-b67e-0afa065242c3 
https://www.albert.io/adaptive/skill/a6c72b24-477a-4500-98f3-90d205b69faf 
https://www.albert.io/adaptive/skill/93677997-d8b1-4917-a7aa-356656ba20e8 
https://www.albert.io/adaptive/skill/55c34e01-9b3d-49d3-bab2-8e33a93c7562 


https://www.albert.io/adaptive/skill/1b7e68ba-9cdb-4f90-80bb-e4ca868a637c 
https://www.albert.io/adaptive/skill/cc4f3231-3faa-4071-a5e6-f7af3dc442ce 
https://www.albert.io/adaptive/skill/cfdc3a7f-a5ec-49a4-befd-f2dd38fc87bd 
https://www.albert.io/adaptive/skill/b8e0fead-7e71-4b27-b633-ed11e82db4f1 
https://www.albert.io/adaptive/skill/890b4394-8b43-4f64-ad06-91c1c1b503fb 

https://www.albert.io/adaptive/skill/60c41ee1-53d5-4ac0-a1e2-e9e88fdb1075 
https://www.albert.io/adaptive/skill/c93382cf-1e87-4182-809f-7515499bf8c6 

Quadratic Functions & Models 
https://www.albert.io/adaptive/skill/4edeec1d-d3b4-468d-b973-4b07d91ede51 
https://www.albert.io/adaptive/skill/c6666a6b-ea0e-477a-a8e1-c458468cbdb8 

https://www.albert.io/adaptive/skill/290ac09c-206b-4708-a681-e5b31fda1319 

https://www.albert.io/adaptive/skill/b8c72681-e050-4344-ad68-3610cd946512 
https://www.albert.io/adaptive/skill/abb6e8a0-1a89-4d30-8f8d-9772c53467df 
https://www.albert.io/adaptive/skill/71b104c9-e623-419b-91bc-7db99ec763c9 

https://www.albert.io/adaptive/skill/ff640494-1171-4dd5-b1a1-690562a91a97 
https://www.albert.io/adaptive/skill/e28d3a9f-bb47-4a58-90a0-2e2d948ac495 

https://www.albert.io/adaptive/skill/4a63757b-f1bc-4c4a-96a3-b644b6b34d36 
https://www.albert.io/adaptive/skill/3647b78c-02db-40ad-a1db-edf5722be7e1 
https://www.albert.io/adaptive/skill/17f3c02d-2363-4f01-92a1-dba4bc32611e 

Radicals & Rational Exponents
https://www.albert.io/adaptive/skill/f02362c8-60f9-4bb0-b145-92518964fc31 

https://www.albert.io/adaptive/skill/c4602096-74de-4ddd-8748-a144af2e49f8 
https://www.albert.io/adaptive/skill/65b01fbf-4054-4d90-88c9-a8f51b2aa6d4 
https://www.albert.io/adaptive/skill/e9cc6756-a29d-47d5-bd89-069269d0e376 


https://www.albert.io/adaptive/skill/0cc6fb3f-3900-43a9-a024-db5cb7085fd4 
https://www.albert.io/adaptive/skill/5e656b2f-922e-4bb4-89f6-2d94435f3e11
https://www.albert.io/adaptive/skill/e29f28dd-8c52-4d5f-8ad6-c886d873221d

https://www.albert.io/adaptive/skill/583cb0f3-18be-47b7-8eee-4809f2fb95d2 
https://www.albert.io/adaptive/skill/3658dbed-e200-4ae5-bed1-66b592720333 
https://www.albert.io/adaptive/skill/89fadddc-b242-458a-8714-0d36b2819828 
https://www.albert.io/adaptive/skill/3e154e3b-3dff-4b56-ace5-bdd63b3ef2fe 

https://www.albert.io/adaptive/skill/ce2b488b-3d9e-4982-a879-e7f60df1aa2c 
https://www.albert.io/adaptive/skill/ea638c9f-bdea-44fc-9d94-f0a744fb2474 
https://www.albert.io/adaptive/skill/b038eced-5ef7-4f94-85cb-044b078594e0 
https://www.albert.io/adaptive/skill/12d49fa7-7fd7-45ea-942f-bbc445aaca2b 

https://www.albert.io/adaptive/skill/b8924597-d26f-476a-8c2f-c5103c874e69
https://www.albert.io/adaptive/skill/dbcc2bd0-c315-41a8-85b1-884959df13a7
https://www.albert.io/adaptive/skill/daf5b97e-a21a-4eb3-8e5c-cbb10d4a364c

Rational & Radical Expressions & Equations
https://www.albert.io/adaptive/skill/b6a89238-b2de-464f-8335-60a4d1f0830c 
https://www.albert.io/adaptive/skill/21249744-ede2-4029-9bee-1e717a1b2e43 
https://www.albert.io/adaptive/skill/c87ce868-48f2-4474-a9e8-bf085fff0259 
https://www.albert.io/adaptive/skill/98a74cc2-e61b-4531-8239-5446ebd96db5 
https://www.albert.io/adaptive/skill/e5b5e5de-9ae2-42e1-8c5c-0007b1b0020f 

https://www.albert.io/adaptive/skill/aeb24c1b-2efb-4fff-ae77-31d9f9a29834 
https://www.albert.io/adaptive/skill/e8418ed0-ebdf-4a6a-a042-e894a59e8938 

https://www.albert.io/adaptive/skill/793fa912-551d-43de-9b0b-8c621915f8cc 
https://www.albert.io/adaptive/skill/ad9ea221-a9ed-415d-99cd-3f95c8c540d4 
https://www.albert.io/adaptive/skill/5ad47925-24be-4641-a77f-07aa7cdfb663 

https://www.albert.io/adaptive/skill/7d65ee6f-8c56-44ab-9e73-7b6f20811dcc 
https://www.albert.io/adaptive/skill/5926885e-e0a5-4018-aaa4-f8c880e825c2
https://www.albert.io/adaptive/skill/1a22e84d-098f-4cfe-8aa9-11615d7e8054 
https://www.albert.io/adaptive/skill/5a0a7153-c942-42c5-b982-0c6d3a6fac92 
https://www.albert.io/adaptive/skill/3e5c0856-56b6-4b53-918c-7638b4c298f5
https://www.albert.io/adaptive/skill/1884e657-db63-457f-b1cf-d394464ffe0b 

https://www.albert.io/adaptive/skill/2936b77d-e4aa-4880-943b-c9bb18347336 
https://www.albert.io/adaptive/skill/14680cd4-c72d-4bb2-8a2b-db7b3ce956e4 
https://www.albert.io/adaptive/skill/2c9aafcd-ea85-48e4-8f22-235a6ab6e38f 
https://www.albert.io/adaptive/skill/e4a027eb-d353-437a-a122-24965795f7d8 
https://www.albert.io/adaptive/skill/0c7d16b7-6f3c-4d71-bc0e-9fa3c330fd90 
https://www.albert.io/adaptive/skill/1fd46c78-8d99-4230-a34b-5defb8b29a70 

https://www.albert.io/adaptive/skill/9a47b9f2-3703-4623-a4c2-209fbf5b13b9 
https://www.albert.io/adaptive/skill/b37e56c6-bb7c-4b89-8117-4b3ea4dd7690 
https://www.albert.io/adaptive/skill/86617a9c-f68d-42c5-8ea2-2481e6420671 
https://www.albert.io/adaptive/skill/5a461850-da78-4ee8-be3b-d5bf40a5a2fa 

https://www.albert.io/adaptive/skill/7d6b7b03-6ea8-4b56-b765-d1f5668daa42 
https://www.albert.io/adaptive/skill/f42df484-b3a1-4006-a1aa-2b2b3e67e351 
https://www.albert.io/adaptive/skill/f14fff28-13c0-4c96-b5ad-3a06f20fe39f 
https://www.albert.io/adaptive/skill/414d38b4-e03f-4519-aecb-5202fe074c51 

Exponential Functions & Models 
https://www.albert.io/adaptive/skill/e24ba9d6-0110-445a-a802-4e691c157a7e 
https://www.albert.io/adaptive/skill/52868af4-e661-4e47-984d-02892a8bf8a9 
https://www.albert.io/adaptive/skill/277c033e-f226-40f7-af80-8f667cd252d7 
https://www.albert.io/adaptive/skill/f1c2314c-1545-45d6-9d13-618c2d2ffa4b 

https://www.albert.io/adaptive/skill/83bb4c61-2791-4c7b-8e33-338e647a0719 
https://www.albert.io/adaptive/skill/a33ed50c-07f3-4fa1-b896-2f0d2087ca27 
https://www.albert.io/adaptive/skill/e1ebdc87-4332-44c8-b82b-4ee869c7ed64 

https://www.albert.io/adaptive/skill/114d4935-ab0a-43e9-8b86-ba7ca7c67824 
https://www.albert.io/adaptive/skill/e8892484-d76d-4efd-9e87-567538475615 
https://www.albert.io/adaptive/skill/6c78a1c5-13da-41e2-abc9-43d8d8ac57d5 

https://www.albert.io/adaptive/skill/4290786c-d8d3-4e94-a33e-d87434116384 

https://www.albert.io/adaptive/skill/516cc4b5-32c2-4be9-b6ed-f4612983eed8 

https://www.albert.io/adaptive/skill/516cc4b5-32c2-4be9-b6ed-f4612983eed8 

https://www.albert.io/adaptive/skill/0160508c-8a05-4bae-811f-e2725e42f350 
https://www.albert.io/adaptive/skill/652564a8-f0d9-44b9-8000-51bd611217dd 
https://www.albert.io/adaptive/skill/cccb8728-5644-4ca5-894a-a73ea8bb09de 

https://www.albert.io/adaptive/skill/6f146c43-63d2-4213-b2a5-0f6c615cab53 

https://www.albert.io/adaptive/skill/73bda0c1-98e7-4b3f-b432-9cbd15caf39e
https://www.albert.io/adaptive/skill/d16dc60b-ec91-43f8-8011-a3c4ab174755 

Exponential & Logarithmic Relationships 

https://www.albert.io/adaptive/skill/4ce3fcfe-eaca-4533-85b9-579935b731d1 
https://www.albert.io/adaptive/skill/e162bc22-c5af-4f45-b2b9-dbc3f14d94aa
https://www.albert.io/adaptive/skill/3d9589a5-f7d8-43dd-b6cc-6f54852dd887 
https://www.albert.io/adaptive/skill/cd80cd21-48ea-4af6-834b-a79c4886ce56 

https://www.albert.io/adaptive/skill/6360a43f-774c-420c-b586-d110bbce0e5c 
https://www.albert.io/adaptive/skill/a0be542a-4cbe-496b-888b-6c260bea2f45 

https://www.albert.io/adaptive/skill/c215775e-26b5-4065-acac-ade87e813e45 
https://www.albert.io/adaptive/skill/ab3853fe-5e4a-4a05-8927-06c9d6b0d60a 
https://www.albert.io/adaptive/skill/59ad16ba-8310-46a5-88e2-95c65d3620af 

https://www.albert.io/adaptive/skill/862a2603-98d9-4d99-978d-bf14c9023fa9 
https://www.albert.io/adaptive/skill/8979652c-1b97-45f8-ab52-9aa4d1281b09 
https://www.albert.io/adaptive/skill/8fc20c3e-3e66-4e06-9707-e3fcb1b81acc 
https://www.albert.io/adaptive/skill/8647f415-db85-4206-9c57-7c7d21425f7a 

https://www.albert.io/adaptive/skill/a249f3e6-ac9f-4f4c-ad13-d5454c1b1f2f 
https://www.albert.io/adaptive/skill/31793c10-9fb1-4dd6-8bbb-7dad0af7252a 
https://www.albert.io/adaptive/skill/8ceaa481-40fb-441e-8454-f61240e18d71 

Logarithmic & Inverse Functions
https://www.albert.io/adaptive/skill/474ae383-8546-495b-9cfc-9a6fec689621 
https://www.albert.io/adaptive/skill/6be3c00f-b8ec-4a52-b1ba-7700e0920ce4 
https://www.albert.io/adaptive/skill/ac58f3ea-d5f6-4e15-8adf-5af02e7b46a5 

https://www.albert.io/adaptive/skill/2c046bd5-7b13-42d7-857a-c9057b56d06b 
https://www.albert.io/adaptive/skill/a94e76f7-afde-493c-85ff-2e363f12ac1d 
https://www.albert.io/adaptive/skill/c5343e45-914f-4c20-a305-5fd86e180ba1 

https://www.albert.io/adaptive/skill/4495eaf6-1bec-4132-8673-8e27923bcc4c 
https://www.albert.io/adaptive/skill/bc979712-2e7e-4a0f-95d6-f90cbd26c770 
https://www.albert.io/adaptive/skill/e731df1f-1b3b-4078-8201-6215b4538922 

https://www.albert.io/adaptive/skill/37d09f0d-059f-4887-93e4-544b5722ba30 
https://www.albert.io/adaptive/skill/13e6502c-2188-48b9-ba46-24ed125bd104 

https://www.albert.io/adaptive/skill/a84ce002-42fe-4b17-a83e-af0caaa6071a 
https://www.albert.io/adaptive/skill/91fd0c47-62e9-49f8-b40d-b41fd57c162c 
https://www.albert.io/adaptive/skill/2785f49b-1584-4854-a196-ba9d53919ae6 

https://www.albert.io/adaptive/skill/cd08ab2c-abd0-42d6-8fd2-a046d12bb71b 


Polynomial & Rational Functions 
https://www.albert.io/adaptive/skill/6f2f4eb3-2bf0-4e0f-993b-f5c20118e1dc 
https://www.albert.io/adaptive/skill/5955f706-2346-48dd-acdd-77881e5b656e 
https://www.albert.io/adaptive/skill/355bb737-e74f-45a6-a51c-439827f8162b 

https://www.albert.io/adaptive/skill/27252d22-d98e-4601-b863-0805830c9384 
https://www.albert.io/adaptive/skill/fd6a67ea-eb42-4554-b753-c15a5b8bbaab 
https://www.albert.io/adaptive/skill/39d8b103-74ca-48c5-b15e-fcff36f1fd9f 
https://www.albert.io/adaptive/skill/75400edf-d6d5-4be3-ab93-79afe44ccb6a 

https://www.albert.io/adaptive/skill/2b47b53f-db2d-472a-bd77-acaf816d5879 
https://www.albert.io/adaptive/skill/2d8f3dd7-e4f6-495a-8697-9bb81c33558a 

https://www.albert.io/adaptive/skill/60b19c73-9d84-4ab5-8eed-36e937c7b21a 

https://www.albert.io/adaptive/skill/59e1ddc6-b035-4f05-aafb-b8c1540d25e6 
https://www.albert.io/adaptive/skill/d0ac0017-c84d-4440-acfa-657a3f348ab2 
https://www.albert.io/adaptive/skill/05a0f464-54ba-4668-9a85-e3a64a80abc2 

https://www.albert.io/adaptive/skill/e861f279-8f31-4539-88e5-224c21400911 
https://www.albert.io/adaptive/skill/a0a6814a-cee7-4fc3-9ddf-f527dd680359 
https://www.albert.io/adaptive/skill/9782b26a-1cd4-413b-b0aa-74d9d5e1f736 
https://www.albert.io/adaptive/skill/e8b5240e-ce12-490f-9f08-7ba5b8e94669 

https://www.albert.io/adaptive/skill/1f882f88-a92e-41b5-ba7e-fc3a59625609 

https://www.albert.io/adaptive/skill/d29cf11c-2c17-4352-8655-fabdaeb70f25 
https://www.albert.io/adaptive/skill/615ad66f-0254-4909-a75a-a64b94b42eb2 

https://www.albert.io/adaptive/skill/95602d73-3917-456d-8617-640c93148bfe 

Function Representations & Transformations 
https://www.albert.io/adaptive/skill/375217b1-efb2-4a97-bd19-f7a1ec311f27 
https://www.albert.io/adaptive/skill/d5859ce9-b126-4c8b-b067-d7ddd3f82b07 
https://www.albert.io/adaptive/skill/6052e275-7c54-4235-b36d-a587a5b71e7c 
https://www.albert.io/adaptive/skill/3ddc3bc5-6fa8-4587-b2af-0a740c6d2119 

https://www.albert.io/adaptive/skill/d5a6d790-d868-4669-8a81-6c4239fa5034 
https://www.albert.io/adaptive/skill/af80b1d0-adf2-4424-bc80-fac6447fe32d 

https://www.albert.io/adaptive/skill/d1ae439a-2ae1-461b-a7e6-96f092b7e69e 
https://www.albert.io/adaptive/skill/de773974-5e44-42ad-88f6-b1b6bb91f509 
https://www.albert.io/adaptive/skill/890d63d6-a710-44e0-86a3-713b2ba7af3b 
https://www.albert.io/adaptive/skill/7d0eb25d-9878-417c-8a79-4cb6b36fcfd7 
https://www.albert.io/adaptive/skill/84ec9e12-c4b0-460d-835b-2595b3dafc24 
https://www.albert.io/adaptive/skill/c48eb22c-c08a-43d6-9918-e0d9c4d5b158 

Complex Numbers 
https://www.albert.io/adaptive/skill/4a717646-ff8c-4939-a4c4-806edbb459e1
https://www.albert.io/adaptive/skill/ece9384c-2fe7-466d-a94d-16673eaf5b35 
https://www.albert.io/adaptive/skill/ceafd45d-912a-4195-bca7-ff34aab1846d 

https://www.albert.io/adaptive/skill/7940e725-66ca-4b04-b67d-da0f9a75af10 
https://www.albert.io/adaptive/skill/68410dd9-bce0-4d72-ba82-7e62aceca498 
https://www.albert.io/adaptive/skill/84348ab8-1757-486e-8a72-1a96bf9cac9c 

https://www.albert.io/adaptive/skill/5ff3fe50-13b1-44d0-83d4-d6b4e44cf82c 
https://www.albert.io/adaptive/skill/cde65ec6-be0e-41b2-9ee1-21d625e0dc4b 
https://www.albert.io/adaptive/skill/6a97c823-2db3-4db0-ba44-8bff64d812fa 



"""

# ─── SELECTORS ────────────────────────────────────────────────────────────────
SEL_LOGIN_EMAIL    = '[data-testid="log-in--identifier"]'
SEL_LOGIN_PASSWORD = '[data-testid="log-in--password"]'
SEL_LOGIN_SUBMIT   = '[type="submit"]'
SEL_TOUR_SKIP      = 'button:has-text("Skip Tour")'
SEL_ALREADY_DONE   = ':text("You achieved \\"Advanced\\" on this skill level!")'
SEL_JUST_DONE      = ':text("You reached the highest level of Advanced for answering 4 of the last 5 correctly!")'

ALBERT_URL_RE = re.compile(r'https://www\.albert\.io/\S+')


def extract_urls(text: str) -> list:
    return [m.rstrip() for m in ALBERT_URL_RE.findall(text)]


def login(page):
    page.goto("https://www.albert.io/log-in")
    page.fill(SEL_LOGIN_EMAIL, EMAIL)
    page.fill(SEL_LOGIN_PASSWORD, PASSWORD)
    time.sleep(0.5)
    page.click(SEL_LOGIN_SUBMIT)
    time.sleep(LOGIN_WAIT)


def check_url(page, url: str) -> bool:
    page.goto(url)
    try:
        page.wait_for_selector(SEL_TOUR_SKIP, timeout=1000)
        page.click(SEL_TOUR_SKIP)
    except TimeoutError:
        pass
    time.sleep(PAGE_LOAD_WAIT)
    return bool(page.query_selector(SEL_ALREADY_DONE) or page.query_selector(SEL_JUST_DONE))


def main():
    urls = extract_urls(URLS_TEXT)
    if not urls:
        print("No albert URLs found in URLS_TEXT.")
        return

    print(f"Checking {len(urls)} albert(s)...\n")

    completed = []
    incomplete = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        print("Logging in...")
        login(page)
        print("Logged in.\n")

        for i, url in enumerate(urls, 1):
            done = check_url(page, url)
            if done:
                completed.append(url)
                print(f"[{i}/{len(urls)}] DONE       {url}")
            else:
                incomplete.append(url)
                print(f"[{i}/{len(urls)}] INCOMPLETE {url}")
            time.sleep(BETWEEN_CHECKS)

        browser.close()

    print(f"\n{'=' * 60}")
    print(f"SUMMARY: {len(completed)} / {len(urls)} completed")
    if incomplete:
        print(f"\nIncomplete ({len(incomplete)}):")
        for url in incomplete:
            print(f"  {url}")
    else:
        print("\nAll alberts are completed!")


if __name__ == "__main__":
    main()
