
/************************** fill the documents inner HTML ***************************/ 
document.body.innerHTML = `
<input type="text" id="email" placeholder="E-Mail" value="test@testmail.com"/>
<input type="text" id="firstname" placeholder="First name" value="Firstname"/>
<input type="text" id="secondname" placeholder="Second name" value="Secondname"/>
<input type="password" id="password" placeholder="Password" value="myPassword123"/>
<input type="password" id="password2" placeholder="Password" value="myPassword123"/>
<input type="text" id="token" placeholder="Token" value="123"/>
`
/*************************************************************************************/

/********************* test the values of the documents inner HTML *******************/ 
test('correct read values of the document HTML', () => {
    expect(document.getElementById("email").value).toBe("test@testmail.com");
    expect(document.getElementById("firstname").value).toBe("Firstname");
    expect(document.getElementById("secondname").value).toBe("Secondname");
    expect(document.getElementById("password").value).toBe("myPassword123");
    expect(document.getElementById("password2").value).toBe("myPassword123");
    expect(document.getElementById("token").value).toBe("123");
});

test('incorrect read value of the document HTML', () => {
    expect(document.getElementById("email").value).not.toBe("test1@testmail.com");
});
/*************************************************************************************/

/****** create a JSON-Object with the values of the documents HTML input values ******/ 
var jsonObj = {};
jsonObj["email"] = "test@test.com";
jsonObj["name"] = "Test User";
jsonObj["password"] = "password123";
jsonObj["token"] = "123";

test('correct created JSON-Object as sent to the server"', () => {
  expect(jsonObj).toMatchObject({email: "test@test.com", name: "Test User", password: "password123", token: "123"});
});
/*************************************************************************************/