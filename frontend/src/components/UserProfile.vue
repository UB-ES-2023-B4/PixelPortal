<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-lg-4">
        <div class="card mb-4">
          <div class="card-body text-center">
            <img
              :src="profilePicture"
              class="rounded-circle img-fluid"
              style="width: 150px; height: 150px"
            />
            <h5 class="my-3">{{ username }}</h5>
            <p
              class="text-muted mb-1 change-color-on-hover"
              @click="seeFollowers"
              style="font-weight: bold"
            >
              {{ followerCount }} Followers {{ followingCount }} Following
            </p>
            <p class="text-muted mb-1">{{ description }}</p>
            <div>
              <p class="text-muted mb-1"></p>
            </div>
            <button
              class="page-button"
              :hidden="!showFollowButton"
              @click="followUser"
            >
              Follow
            </button>
            <button
              class="page-button"
              :hidden="!showUnfollowButton"
              @click="unfollowUser"
            >
              Unfollow
            </button>
            <!--
                          <div class="d-flex justify-content-center mb-2">
                              <button type="button" class="btn btn-primary">Edit Profile</button>
                          </div>
                          -->
          </div>
        </div>
        <div class="card mb-4 mb-lg-0">
          <div class="card-body p-0">
            <ul class="list-group list-group-flush rounded-3">
              <router-link
                :hidden="!isLoggedInUserProfile"
                :to="{
                  name: 'editProfile',
                  params: { id: this.userID },
                  query: {
                    token: this.token,
                    loggedUsername: this.username,
                  },
                }"
              >
                <li
                  class="custom-list-group-item d-flex justify-content-between align-items-center p-3"
                >
                  <img
                    src="../assets/editar.png"
                    alt="Icono personalizado"
                    class="custom-icon"
                  />
                  <p class="mb-0" style="text-align: center; color: black">
                    Edit Profile
                  </p>
                </li>
              </router-link>
              <li
                @click="seeBookmarks()"
                class="custom-list-group-item d-flex justify-content-between align-items-center p-3"
              >
                <img
                  src="../assets/marcador.png"
                  alt="Icono personalizado"
                  class="custom-icon"
                />
                <p class="mb-0">Bookmarks</p>
              </li>
              <li
                class="custom-list-group-item d-flex justify-content-between align-items-center p-3"
                @click="showUploadImageForm = true"
              >
                <img
                  src="../assets/agregar.png"
                  alt="Icono personalizado"
                  class="custom-icon"
                />
                <p class="mb-0">New Post</p>
              </li>
              <router-link
                :hidden="!isLoggedInUserProfile"
                :to="{
                  name: 'changePassword',
                  params: { id: this.userID },
                  query: {
                    token: this.token,
                    loggedUsername: this.username,
                  },
                }"
              >
                <li
                  class="custom-list-group-item d-flex justify-content-between align-items-center p-3"
                >
                  <img
                    src="../assets/fingerprint.png"
                    alt="Icono personalizado"
                    class="custom-icon"
                  />
                  <p class="mb-0" style="text-align: center; color: black">
                    Change Password
                  </p>
                </li>
              </router-link>
              <li
                class="custom-list-group-item d-flex justify-content-between align-items-center p-3"
                @click="redirectToMainPage"
              >
                <img
                  src="../assets/casa.png"
                  alt="Icono personalizado"
                  class="custom-icon"
                />
                <p class="mb-0">Home</p>
              </li>
            </ul>
            <div :hidden="!isLoggedInUserProfile">
              <li
                class="custom-list-group-item d-flex justify-content-between align-items-center p-3"
                @click="deleteAccount"
              >
                <img
                  src="../assets/person-x.svg"
                  alt="Icono personalizado"
                  class="custom-icon"
                />
                <p class="mb-0">Delete Account</p>
              </li>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-8" v-if="!isFollowersClicked && !isBookmarksClicked">
        <div class="image-container">
          <UploadImagePopup
            :open="showUploadImageForm"
            :username="username"
            :token="token"
            @close="closeUploadImageForm"
          >
          </UploadImagePopup>
          <div class="images">
            <div
              class="image-card"
              v-for="img in showMyImages ? currentUserImages : filteredList"
              :key="img.id"
              :data-name="img.username"
            >
              <router-link
                :to="{
                  name: 'postZoom',
                  params: { id: img.id },
                  query: {
                    token: this.token,
                    loggedUserID: this.id,
                  },
                }"
              >
                <img :src="img.image" />
              </router-link>
              <h6 class="image-title">{{ img.title }}</h6>
              <h6 class="image-username">{{ img.username }}</h6>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-8" v-if="isBookmarksClicked">
        <div class="circle-container">
          <button
            type="button"
            class="btn-close"
            aria-label="Close"
            @click="closeBookmarks()"
          ></button>
        </div>
        <div class="image-container">
          <div class="images">
            <div
              class="image-card"
              v-for="img in bookmarksList"
              :key="img.id"
              :data-name="img.username"
            >
              <router-link
                :to="{
                  name: 'postZoom',
                  params: { id: img.id },
                  query: {
                    token: this.token,
                    loggedUserID: this.id,
                  },
                }"
              >
                <img :src="img.image" />
              </router-link>
              <h6 class="image-title">{{ img.title }}</h6>
              <h6 class="image-username">{{ img.username }}</h6>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-8" v-if="isFollowersClicked">
        <div
          class="text-center"
          style="align-items: center; align-content: center; display: flex"
        >
          <div class="e-btn-group">
            <input
              type="radio"
              id="radioleft"
              name="align"
              value="left"
              checked
              v-model="selectedOption"
            />
            <label class="e-btn" for="radioleft">Followers</label>
            <input
              type="radio"
              id="radiomiddle"
              name="align"
              value="right"
              v-model="selectedOption"
            />
            <label class="e-btn" for="radiomiddle">Following</label>
          </div>
          <div class="circle-container">
            <button
              type="button"
              class="btn-close"
              aria-label="Close"
              @click="closeFollowers()"
            ></button>
          </div>
        </div>
        <div v-if="selectedOption === 'left'" class="follower-container">
          <div
            class="follower"
            v-for="follower in followersList"
            :key="follower.id"
            :data-name="follower.name"
          >
            <div class="user-card">
              <div class="image-content">
                <span class="overlay"></span>
                <div class="card-image">
                  <img :src="follower.image" alt="" class="card-img" />
                </div>
              </div>
              <div class="card-content">
                <h2 class="name">{{ follower.name }}</h2>
                <p class="description">{{ follower.description }}</p>
              </div>
            </div>
          </div>
        </div>
        <div v-if="selectedOption === 'right'" class="follower-container">
          <div
            class="follow"
            v-for="follow in followingList"
            :key="follow.id"
            :data-name="follow.name"
          >
            <div class="user-card">
              <div class="image-content">
                <span class="overlay"></span>
                <div class="card-image">
                  <img :src="follow.image" alt="" class="card-img" />
                </div>
              </div>
              <div class="card-content">
                <h2 class="name">{{ follow.name }}</h2>
                <p class="description">{{ follow.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { storage } from "@/firebase";
import { ref as firebaseRef, getDownloadURL } from "firebase/storage";
import UploadImagePopup from "./UploadImagePopup.vue";
import axios from "axios";

export default {
  name: "PostZoom",
  components: { UploadImagePopup },
  setup() {
    const showUploadImageForm = ref(false);
    return { showUploadImageForm };
  },
  data() {
    return {
      id: parseInt(this.$route.params.id),
      username: "",
      token: this.$route.query.token,
      loggedInUserID: parseInt(this.$route.query.loggedUserID),
      description: "",
      profilePicture: "",
      leftSidebarMinimized: false,
      musicPlayerVisible: false,
      timerDisplayVisible: false,
      directMessagingVisible: false,
      imageList: [],
      currentUserImages: [],
      bookmarksList: [],
      showMyImages: false,
      isLoggedInUserProfile: false,
      isFollowersClicked: false,
      isFollowingClicked: false,
      isBookmarksClicked: false,
      isLoggedInUserFollowingUser: false,
      selectedOption: "left",
      followerCount: 0,
      followingCount: 0,
      followersList: [],
      followingList: [],
      followerPicture: "",
      renderComponent: true,
    };
  },
  computed: {
    filteredList() {
      return this.imageList.filter((img) => {
        return img.username == this.username;
      });
    },
    showFollowButton() {
      return !this.isLoggedInUserFollowingUser && !this.isLoggedInUserProfile;
    },
    showUnfollowButton() {
      return this.isLoggedInUserFollowingUser && !this.isLoggedInUserProfile;
    },
  },
  methods: {
    redirectToMainPage() {
      history.back();
    },
    seeFollowers() {
      this.isFollowersClicked = true;
    },
    seeFollowing() {
      this.isFollowingClicked = true;
    },
    seeBookmarks() {
      this.isBookmarksClicked = true;
    },
    closeBookmarks() {
      this.isBookmarksClicked = false;
    },
    closeFollowers() {
      this.isFollowersClicked = false;
    },
    closeFollowing() {
      this.isFollowingClicked = false;
    },
    getUserInfo(userID) {
      this.userID = userID;
      const pathUser = this.backendPath + "/usuario/" + this.userID;
      axios
        .get(pathUser)
        .then((response) => {
          this.username = response.data.nombre;
          this.description = response.data.descripcion;
          const profilePictureRef = firebaseRef(
            storage,
            response.data.imagen_perfil_url
          );
          getDownloadURL(profilePictureRef).then((url) => {
            this.profilePicture = url;
          });
        })
        .catch((error) => {
          console.error(error);
        });
    },
    closeUploadImageForm(data) {
      this.showUploadImageForm = false;
      this.postedImageID = data.imageID;
      //Check if image has been posted
      if (data.hasPosted) {
        //post image with all the data + the image ID to the backend DATABASE here
        const path = this.backendPath + "/publicaciones";
        const headers = { Authorization: "Bearer " + this.token };
        const dbData = {
          titulo: data.imageTitle,
          descripcion: data.imageDescription,
          imagen_url: data.imageID,
          usuario_nombre: data.username,
          tags: JSON.stringify(data.imageTags),
        };
        axios
          .post(path, dbData, { headers })
          .then((response) => {
            if (response.status === 200) {
              alert("Image uploaded successfully!");
              this.getPublication();
            }
          })
          .catch((error) => {
            alert("Error: " + error.response.data.message);
          });
      }
    },
    getPublication() {
      this.imageList = [];
      this.currentUserImages = []; // Agregar esta línea

      const pathPublications = this.backendPath + "/publicaciones";

      axios
        .get(pathPublications)
        .then((res) => {
          var publications = res.data.filter((publi) => {
            return publi.id != null;
          });
          for (let i = 0; i < publications.length; i++) {
            // Use publication data to recover image from Firebase and create the card
            const postedImageRef = firebaseRef(
              storage,
              "postedImages/" + publications[i].imagen_url
            );
            getDownloadURL(postedImageRef).then((url) => {
              let image = {
                id: publications[i].id,
                image: url,
                description: publications[i].descripcion,
                title: publications[i].titulo,
                username: publications[i].usuario_nombre,
                postDate: publications[i].fecha_creacion,
                postTags: JSON.parse(publications[i].tags),
              };
              this.imageList.push(image);

              // Verifica si la imagen pertenece al usuario actual y agrégala a currentUserImages
              if (image.username === this.username) {
                this.currentUserImages.push(image);
              }
            });
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getBookmarks(userID) {
      this.imageList = [];
      this.currentUserImages = []; // Agregar esta línea

      const pathPublications = this.backendPath + "/bookmarks/user/" + userID;

      axios
        .get(pathPublications)
        .then((res) => {
          var publications = res.data.filter((publi) => {
            return publi.id != null;
          });
          for (let i = 0; i < publications.length; i++) {
            // Use publication data to recover image from Firebase and create the card
            const postedImageRef = firebaseRef(
              storage,
              "postedImages/" + publications[i].imagen_url
            );
            getDownloadURL(postedImageRef).then((url) => {
              let image = {
                id: publications[i].id,
                image: url,
                description: publications[i].descripcion,
                title: publications[i].titulo,
                username: publications[i].usuario_nombre,
                postDate: publications[i].fecha_creacion,
                postTags: JSON.parse(publications[i].tags),
              };
              this.bookmarksList.push(image);
            });
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getFollowers(userID) {
      this.followersList = [];

      const pathUsers = this.backendPath + "/usuario/" + userID + "/followers";

      axios.get(pathUsers).then((res) => {
        this.isLoggedInUserFollowingUser = res.data.some(
          (item) => item.id === this.loggedInUserID
        );
        this.followerCount = res.data.length;
        var followers = res.data.filter((follower) => {
          return follower.id != null;
        });
        for (let i = 0; i < followers.length; i++) {
          const profilePicRef = firebaseRef(
            storage,
            followers[i].imagen_perfil_url
          );

          getDownloadURL(profilePicRef).then((url) => {
            let follower = {
              id: followers[i].id,
              name: followers[i].nombre,
              description: followers[i].descripcion,
              image: url,
            };

            if (follower.description === "") {
              follower.description = "User has no description";
            }

            this.followersList.push(follower);
          });
        }
      });
    },
    getFollowing(userID) {
      this.followingList = [];

      const pathUsers = this.backendPath + "/usuario/" + userID + "/following";

      axios.get(pathUsers).then((res) => {
        this.followingCount = res.data.length;
        var following = res.data.filter((follow) => {
          return follow.id != null;
        });
        for (let i = 0; i < following.length; i++) {
          const profilePicRef = firebaseRef(
            storage,
            following[i].imagen_perfil_url
          );

          getDownloadURL(profilePicRef).then((url) => {
            let follow = {
              id: following[i].id,
              name: following[i].nombre,
              description: following[i].descripcion,
              image: url,
            };

            if (follow.description === "") {
              follow.description = "User has no description";
            }

            this.followingList.push(follow);
          });
        }
      });
    },
    followUser() {
      const followUserPath =
        this.backendPath +
        "/usuario/" +
        this.id +
        "/follow/" +
        this.loggedInUserID;
      axios
        .post(followUserPath)
        .then(() => {
          this.getFollowers(this.userID);
        })
        .catch((error) => {
          console.log(error.message);
        });
    },
    unfollowUser() {
      const unfollowUserPath =
        this.backendPath +
        "/usuario/" +
        this.id +
        "/unfollow/" +
        this.loggedInUserID;
      axios
        .delete(unfollowUserPath)
        .then(() => {
          this.getFollowers(this.userID);
        })
        .catch((error) => {
          console.log(error.message);
        });
    },
    deleteAccount() {
      if (confirm("Are you sure you want to delete this account?")) {
        const deleteAccountPath =
          this.backendPath + "/usuario/" + this.loggedInUserID;
        axios
          .delete(deleteAccountPath)
          .then(() => {
            this.$router.push("/");
          })
          .catch((error) => {
            console.log(error.message);
          });
      }
    },
  },
  mounted() {
    window.addEventListener("click", this.closeDropdown);
    this.getPublication();
    this.getBookmarks(this.$route.params.id);
  },
  beforeUnmount() {
    window.removeEventListener("click", this.closeDropdown);
  },
  created() {
    this.token = this.$route.query.token;
    if (this.loggedInUserID === this.id) {
      this.isLoggedInUserProfile = true;
    }
    if (typeof this.token === "undefined") {
      this.$router.push({ path: "/" });
    } else {
      this.getUserInfo(this.$route.params.id);
      this.getFollowers(this.$route.params.id);
      this.getFollowing(this.$route.params.id);
    }
  },
};
</script>

<style scoped>
@import "../../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../../node_modules/@syncfusion/ej2-buttons/styles/material.css";
@import "../../node_modules/@syncfusion/ej2-popups/styles/material.css";
@import "../../node_modules/@syncfusion/ej2-splitbuttons/styles/material.css";

body {
  background-color: #b3e5fc;
  border-radius: 10px;
}

/* Estilo predeterminado para las etiquetas de botón */
.e-btn {
  padding: 8px 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

.follower-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between; /* Espacio entre las tarjetas */
}
.circle-container {
  width: 40px;
  /* Ancho del círculo */
  height: 40px;
  /* Altura del círculo */
  border-radius: 50%;
  /* Borde redondeado para hacer un círculo */
  background-color: #cccccc95;
  /* Color de fondo del círculo */
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background-color 0.3s;
  /* Transición suave del color de fondo */
}

.circle-container:hover {
  color: rgba(20, 117, 236, 0.9);
  background-color: rgba(20, 117, 236, 0.9);
}

.btn-close {
  background-color: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
}

.change-color-on-hover:hover {
  color: rgba(20, 117, 236, 0.9);
}

.e-btn:hover {
  background-color: rgba(211, 231, 255, 0.9);
  /* Cambia a un color claro al pasar el cursor */
}

/* Estilo cuando el radio está seleccionado */
input[type="radio"]:checked + .e-btn {
  background-color: rgba(20, 117, 236, 0.9);
  color: white;
}

.e-btn-group {
  margin: 25px 5px 20px 20px;
  align-content: center;
  align-items: center;
  align-self: center;
  text-align: center;
  margin-left: auto;
  margin-right: auto;
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
  width: 280px;
  height: 280px;
  box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.3);
  margin-bottom: 10px;
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

.stats {
  background: #f2f5f8 !important;

  color: #000 !important;
}

.articles {
  font-size: 10px;
  color: #a1aab9;
}

.number1 {
  font-weight: 500;
}

.followers {
  font-size: 10px;
  color: #a1aab9;
}

.number2 {
  font-weight: 500;
}

.rating {
  font-size: 10px;
  color: #a1aab9;
}

.number3 {
  font-weight: 500;
}

.custom-list-group-item:hover {
  background-color: #178fff;
  /* Color de fondo oscuro */
  color: #fff;
  /* Color de texto blanco */
  /* Otros estilos adicionales, como sombras u otros cambios de diseño */
}

.custom-icon {
  height: 2em;
  width: 2em;
}

.image-container {
  position: relative;
  min-height: 100vh;
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #fff;
}

.image-container .search-box {
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

.image-container .images .image-card {
  position: relative;
  height: 300px;
  width: 210px;
  border-radius: 6px;
  overflow: hidden;
}

.custom-text-center {
  text-align: center;
}

.images {
  width: 100%;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.images .image-card {
  margin: 8px;
}

.images .image-card img {
  height: 100%;
  width: 100%;
  max-height: 100%;
  max-width: 100%;
  border-radius: 6px;
  transition: transform 0.2s linear;
}

.image-card:hover img {
  transform: scale(1.15);
}

.image-container .images .image-title {
  position: absolute;
  bottom: 30px;
  left: 10px;
  color: #fff;
  font-size: 24px;
  font-weight: 400;
  text-transform: capitalize;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 3px;
}

.image-container .images .image-username {
  position: absolute;
  bottom: 7.1px;
  left: 10px;
  color: #fff;
  font-size: 20px;
  font-weight: 400;
  text-transform: capitalize;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 3px;
}

.profile-picture {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 8px;
}

/* Style the dropdown button and content */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  position: absolute;
  background-color: white;
  min-width: 100px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #f1f1f1;
}

.page-button {
  background-color: rgba(20, 117, 236, 0.9);
  color: white;
  height: 45px;
  width: 8rem;
  margin: 10px;
  border-radius: 6px;
}
</style>
