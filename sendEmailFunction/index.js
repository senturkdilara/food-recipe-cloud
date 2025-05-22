const nodemailer = require("nodemailer");

exports.sendEmail = async (req, res) => {
  // Enable CORS
  res.set("Access-Control-Allow-Origin", "*");
  res.set("Access-Control-Allow-Methods", "POST");
  res.set("Access-Control-Allow-Headers", "Content-Type");

  // Handle preflight OPTIONS request
  if (req.method === "OPTIONS") {
    return res.status(204).send("");
  }

  const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
      user: process.env.EMAIL_USER,  // e.g., dilarasenturk069@gmail.com
      pass: process.env.EMAIL_PASS,  // App password from Gmail
    },
  });

  try {
    await transporter.sendMail({
      from: process.env.EMAIL_USER,
      to: "senturkdilara@sabanciuniv.edu",
      subject: "Login Successful",   
      text: "You have successfully logged in to your Food Blog app.",
    });

    res.status(200).send(" email sent successfully");
  } catch (err) {
    console.error("Email error:", err);
    res.status(500).send("Failed to send hardcoded email");
  }
};

