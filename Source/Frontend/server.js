const path = require("path")
const express = require("express")
const app = express()

app.set('views', path.join(__dirname, '/public/views'));
app.set("view engine", "ejs")

app.use(express.static(__dirname + '/public'));

app.get("/", (req, res) => {
    res.render("index")
})

app.listen(5000)