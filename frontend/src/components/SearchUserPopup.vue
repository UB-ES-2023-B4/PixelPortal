<template>
  <transition name="fade">
    <div class="popup" v-show="open">
      <link
        rel="stylesheet"
        href="https://unicons.iconscout.com/release/v4.0.0/css/thinline.css"
      />
      <transition name="drop-in">
        <div class="popup-inner" v-show="open">
          <div class="popup-content">
            <h1 class="title">Search User</h1>
            <div class="search-box">
              <i class="bx bx-search"></i>
              <input type="text" v-model="search" placeholder="Search" />
            </div>
            <div class="user-container">
              <div
                class="user"
                v-for="user in filteredList"
                :key="user.id"
                :data-name="user.name"
              >
                <router-link
                  style="text-decoration: none; color: inherit"
                  :to="{
                    name: 'userProfile',
                    params: { id: user.id },
                    query: {
                      token: this.token,
                      loggedUserID: this.loggedInUserID,
                    },
                  }"
                >
                  <div class="user-card">
                    <div class="image-content">
                      <span class="overlay"></span>
                      <div class="card-image">
                        <img :src="user.image" alt="" class="card-img" />
                      </div>
                    </div>
                    <div class="card-content">
                      <h2 class="name">{{ user.name }}</h2>
                      <p class="description">{{ user.description }}</p>
                    </div>
                  </div>
                </router-link>
              </div>
            </div>
            <button type="button" class="popup-button" @click="closeComponent">
              Close
            </button>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>

<script>
import { ref, getDownloadURL } from "firebase/storage";
import axios from "axios";
import { storage } from "@/firebase";
export default {
  name: "SearchUserPopup",
  props: {
    open: {
      type: Boolean,
      required: true,
    },
    loggedInUserID: {
      type: Number,
      required: true,
    },
    token: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      search: "",
      userList: [],
    };
  },
  computed: {
    filteredList() {
      if (this.search.length > 0) {
        const searchTerm = this.search.toLowerCase();
        return this.userList.filter((user) => {
          return user.name.toLowerCase().includes(searchTerm);
        });
      } else {
        return this.userList;
      }
    },
  },
  methods: {
    resetValues() {},
    closeComponent() {
      this.resetValues();
      this.$emit("close");
    },
    getUsers() {
      this.userList = [];

      const pathUsers = this.backendPath + "/usuarios";

      axios.get(pathUsers).then((res) => {
        var users = res.data.filter((user) => {
          return user.id != null;
        });
        for (let i = 0; i < users.length; i++) {
          const profilePicRef = ref(storage, users[i].imagen_perfil_url);

          getDownloadURL(profilePicRef).then((url) => {
            let user = {
              id: users[i].id,
              name: users[i].nombre,
              description: users[i].descripcion,
              image: url,
            };

            if (user.description === "") {
              user.description = "User has no description";
            }

            this.userList.push(user);
          });
        }
      });
    },
  },
  created() {
    this.getUsers();
  },
};
</script>

<style scoped>
*,
::before,
::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  overflow-y: auto;
  z-index: 3;
  background-color: rgba(0, 0, 0, 0.6);
}

.popup-inner {
  max-width: 1000px;
  margin: 2rem auto;
}

.popup-content {
  position: relative;
  background-color: #efefef;
  border: 1px solid rgba(0, 0, 0, 0.3);
  background-clip: padding-box;
  border-radius: 0.3rem;
  padding: 1rem;
}
.title {
  font-weight: 600;
}
.user-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  position: relative;
  max-height: 10px;
  overflow-y: auto;
  min-height: 80vh;
  max-width: 100%;
  width: 100%;
  margin: 10px;
  padding: 40px 20px;
  background-color: #efefef;
}

.search-box {
  margin: 10px;
  position: relative;
  height: 42px;
  max-width: 400px;
  margin: 0 auto;
  margin-bottom: 40px;
}

.search-box input {
  position: absolute;
  height: 100%;
  width: 100%;
  outline: none;
  border: none;
  background-color: #323334;
  padding: 0 15px 0 45px;
  color: #fff;
  border-radius: 6px;
  font-size: 20px;
}

.search-box i {
  position: absolute;
  z-index: 2;
  color: #999;
  top: 50%;
  left: 15px;
  font-size: 20px;
  transform: translateY(-50%);
}

.user {
  margin-bottom: 10px;
}

.user-card {
  background-color: white;
  border-radius: 25px;
  width: 320px;
}

.image-content,
.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 14px;
}

.image-content {
  position: relative;
  row-gap: 5px;
}
.card-image {
  position: relative;
  height: 150px;
  width: 150px;
  border-radius: 50%;
}

.card-image .card-img {
  height: 100%;
  width: 100%;
  object-fit: cover;
  border-radius: 50%;
  border: 4px solid rgba(20, 117, 236, 0.9);
}

.name {
  font-size: 24px;
  font-weight: 700;
}

.description {
  font-size: 18px;
  color: #707070;
  text-align: center;
}

.overlay {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 100%;
  background-color: rgba(20, 117, 236, 0.9);
  border-radius: 25px 25px 0 0;
}
.popup-button {
  background-color: rgba(20, 117, 236, 0.9);
  color: white;
  height: 45px;
  width: 8rem;
  margin: 10px;
  border-radius: 6px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.drop-in-enter-active,
.drop-in-leave-active {
  transition: all 0.3s ease-out;
}

.drop-in-enter-from,
.drop-in-leave-to {
  opacity: 0;
  transform: translateY(-50px);
}
</style>
