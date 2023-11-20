<template>
  <div>
    <div class="row">
      <h1
        style="
          font-size: 50px;
          font-weight: bolder;
          text-align: center;
          margin-top: 3%;
        "
      >
        PixelPortal
      </h1>
    </div>
    <div class="row" style="margin-top: 300px">
      <div class="login-reg-panel">
        <div class="login-info-box" v-show="!isLoginChecked">
          <h2>Have an account?</h2>
          <p>Frame Your Memories, Log In!</p>
          <label
            id="label-register"
            for="log-reg-show"
            style="border-color: white"
            >Login</label
          >
          <input
            type="radio"
            name="active-log-panel"
            id="log-reg-show"
            checked="checked"
          />
        </div>

        <div class="register-info-box" v-show="isLoginChecked">
          <h2>Don't have an account?</h2>
          <p>Start Your Photographic Journey!</p>
          <label
            id="label-login"
            for="log-login-show"
            style="border-color: white"
            >Sign Up</label
          >
          <input type="radio" name="active-log-panel" id="log-login-show" />
        </div>

        <div class="white-panel">
          <div class="login-show">
            <h2 style="font-weight: bold">LOGIN</h2>
            <input 
              type="text" 
              placeholder="Username" 
              v-model="loginEmail"
            />
            <input
              type="password"
              placeholder="Password"
              v-model="loginPassword"
            />
            <input
              type="button"
              value="Login"
              @click="checkLogin"
            />
            <a href="">Forgot password?</a>
          </div>
          <div class="register-show">
            <h2 style="font-weight: bold">SIGN UP</h2>
            <input
              type="text"
              placeholder="Username"
              v-model="signUpUsername"
            />
            <input
              type="text"
              placeholder="Email"
              v-model="signUpEmail"
            />
            <input
              type="password"
              placeholder="Password"
              v-model="signUpPassword"
            />
            <input
              type="password"
              placeholder="Confirm Password"
              v-model="signUpConfirmPassword"
            />
            <input
              type="button"
              value="Sign Up"
              @click="checkSignup"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from "jquery"; // Importa jQuery
import axios from "axios";

export default {
  name: "LoginRegister",
  data() {
    return {
      isLoginChecked: true,
      loginEmail: "",
      loginPassword: "",
      signUpUsername: "",
      signUpEmail: "",
      signUpPassword: "",
      signUpConfirmPassword: "",
    };
  },
  mounted() {
    // Este código se ejecutará después de que el componente se haya montado

    $(".login-info-box").hide();
    $(".login-show").addClass("show-log-panel");

    $('.login-reg-panel input[type="radio"]').on("change", () => {
      if ($("#log-login-show").is(":checked")) {
        $(".register-info-box").hide();
        $(".login-info-box").show();

        $(".white-panel").addClass("right-log");
        $(".register-show").addClass("show-log-panel");
        $(".login-show").removeClass("show-log-panel");
      } else if ($("#log-reg-show").is(":checked")) {
        $(".register-info-box").show();
        $(".login-info-box").hide();

        $(".white-panel").removeClass("right-log");

        $(".login-show").addClass("show-log-panel");
        $(".register-show").removeClass("show-log-panel");
      }
    });
  },
  methods: {
    checkLogin() {
      const path = this.backendPath + "/login";
      const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
      if (emailRegex.test(this.loginEmail)) {
        axios
          .post(path, {
            email: this.loginEmail,
            contrasena: this.loginPassword,
          })
          .then((response) => {
            this.$router.push({
              path: "/home",
              query: {
                user_id: response.data.user_id,
                token: response.data.access_token,
              },
            });
          })
          .catch((error) => {
            alert("Error: " + error.response.data.detail);
          });
      } else {
        alert("Email is not valid");
      }
    },
    checkSignup() {
      if (this.signUpPassword != this.signUpConfirmPassword) {
        alert("Passwords do not match");
      } else {
        const path = this.backendPath + "/usuario";
        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        if (emailRegex.test(this.signUpEmail)) {
          axios
            .post(path, {
              nombre: this.signUpUsername,
              email: this.signUpEmail,
              contrasena: this.signUpPassword,
              descripcion: "",
              imagen_perfil_url: "profilePictures/default_PFP.png",
            })
            .then((response) => {
              if (response.status == 200) {
                this.$router.push({
                  path: "/home",
                  query: {
                    user_id: response.data.user.id,
                    token: response.data.access_token.access_token,
                  },
                });
              }
            })
            .catch((error) => {
              alert("Error: " + error.response.data.detail);
            });
        } else {
          alert("Email is not valid");
        }
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("https://fonts.googleapis.com/css?family=Mukta");

body {
  font-family: "Mukta", sans-serif;
  height: 100vh;
  min-height: 550px;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  position: relative;
  overflow-y: hidden;
}

a {
  text-decoration: none;
  color: #444444;
}

.login-reg-panel {
  position: relative;
  top: 50%;
  transform: translateY(-50%);
  text-align: center;
  width: 70%;
  right: 0;
  left: 0;
  margin: auto;
  height: 400px;
  background-color: rgba(20, 117, 236, 0.9);
}

.white-panel {
  background-color: rgba(255, 255, 255, 1);
  height: 500px;
  position: absolute;
  top: -50px;
  width: 50%;
  right: calc(50% - 50px);
  transition: 0.3s ease-in-out;
  z-index: 0;
  box-shadow: 0 0 15px 9px #00000096;
}

.login-reg-panel input[type="radio"] {
  position: relative;
  display: none;
}

.login-reg-panel {
  color: #b8b8b8;
}

.login-reg-panel #label-login,
.login-reg-panel #label-register {
  border: 1px solid #9e9e9e;
  padding: 5px 5px;
  width: 150px;
  display: block;
  text-align: center;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 18px;
}

.login-info-box {
  width: 30%;
  padding: 0 50px;
  top: 20%;
  left: 0;
  position: absolute;
  text-align: left;
  color: white;
}

.register-info-box {
  width: 30%;
  padding: 0 50px;
  top: 20%;
  right: 0;
  position: absolute;
  text-align: left;
  color: white;
}

.right-log {
  right: 50px !important;
}

.login-show,
.register-show {
  z-index: 1;
  display: none;
  opacity: 0;
  transition: 0.3s ease-in-out;
  color: #242424;
  text-align: left;
  padding: 50px;
}

.show-log-panel {
  display: block;
  opacity: 0.9;
}

.login-show input[type="text"],
.login-show input[type="password"] {
  width: 100%;
  display: block;
  margin: 20px 0;
  padding: 15px;
  border: 1px solid #b5b5b5;
  outline: none;
}

.login-show input[type="button"] {
  max-width: 150px;
  width: 100%;
  background: #444444;
  color: #f9f9f9;
  border: none;
  padding: 10px;
  text-transform: uppercase;
  border-radius: 2px;
  float: right;
  cursor: pointer;
}

.login-show a {
  display: inline-block;
  padding: 10px 0;
}

.register-show input[type="text"],
.register-show input[type="password"] {
  width: 100%;
  display: block;
  margin: 20px 0;
  padding: 15px;
  border: 1px solid #b5b5b5;
  outline: none;
}

.register-show input[type="button"] {
  max-width: 150px;
  width: 100%;
  background: #444444;
  color: #f9f9f9;
  border: none;
  padding: 10px;
  text-transform: uppercase;
  border-radius: 2px;
  float: right;
  cursor: pointer;
}

.credit {
  position: absolute;
  bottom: 10px;
  left: 10px;
  color: #3b3b25;
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  text-transform: uppercase;
  font-size: 12px;
  font-weight: bold;
  letter-spacing: 1px;
  z-index: 99;
}

a {
  text-decoration: none;
  color: #2c7715;
}
</style>
