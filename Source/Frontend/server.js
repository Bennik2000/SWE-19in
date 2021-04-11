const path = require("path")
const express = require("express")
const app = express()

app.set('views', path.join(__dirname, '/public/views'));
app.set("view engine", "ejs")

app.use(express.static(__dirname + '/public'));

app.get("/", (req, res) => {
    res.render("index")
})

app.get("/loginpage", (req, res) => {
    res.render("loginpage")
})

app.get("/reset_password", (req, res) => {
    res.render("reset_password")
})

app.get("/create_account", (req, res) => {
    res.render("create_account")
})

app.get("/account", (req, res) => {
    res.render("personal_account_space")
})
app.listen(5000)