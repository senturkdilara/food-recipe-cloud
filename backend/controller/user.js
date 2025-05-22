const User = require("../models/user")
const bcrypt = require("bcrypt")
const jwt = require("jsonwebtoken")

const userSignUp = async (req, res) => {
    const { email, password } = req.body
    if (!email || !password) {
        return res.status(400).json({ message: "Email and password is required" })
    }
    let user = await User.findOne({ email })
    if (user) {
        return res.status(400).json({ error: "Email is already exist" })
    }
    const hashPwd = await bcrypt.hash(password, 10)
    const newUser = await User.create({
        email, password: hashPwd
    })
    let token = jwt.sign({ email, id: newUser._id }, process.env.SECRET_KEY)
    return res.status(200).json({ token, user:newUser })

}

const axios = require('axios');

const userLogin = async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ message: "Email and password is required" });
  }
  
  let user = await User.findOne({ email });
  
  if (user && await bcrypt.compare(password, user.password)) {
    // Sign JWT token
    let token = jwt.sign({ email, id: user._id }, process.env.SECRET_KEY);
    // Call Cloud Function to send email notification
    try {
      fetch("https://us-central1-food-recipe-cloud.cloudfunctions.net/sendEmail", {
          method: "POST"
        })
    } catch (error) {
      console.error('Error calling email Cloud Function:', error.message);
      // You can decide whether to fail login or just log the error
    }    
    return res.status(200).json({ token, user });
  } else {
    return res.status(400).json({ error: "Invalid credentials" });
  }
};

const getUser = async (req, res) => {
    const user = await User.findById(req.params.id)
    res.json({email:user.email})
}

module.exports = { userLogin, userSignUp, getUser }
