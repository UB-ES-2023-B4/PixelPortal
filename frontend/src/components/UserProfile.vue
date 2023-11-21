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
            <p class="text-muted mb-1" data-cy="check-follow">
              {{ followerCount }} Followers {{ followingCount }} Following
            </p>
            <p class="text-muted mb-1" data-cy="user-description">{{ description }}</p>
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
                  data-cy="edit-profile"
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
              <li
                class="custom-list-group-item d-flex justify-content-between align-items-center p-3"
                data-cy="home-button"
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
          </div>
        </div>
      </div>
      <div class="col-lg-8">
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
      showMyImages: false,
      isLoggedInUserProfile: false,
      isLoggedInUserFollowingUser: false,
      followerCount: 0,
      followingCount: 0,
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
    getUserInfo() {
      this.userID = this.$route.params.id;
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
    getFollowers() {
      const followersPath =
        this.backendPath + "/usuario/" + this.id + "/followers";
      axios.get(followersPath).then((response) => {
        this.isLoggedInUserFollowingUser = response.data.some(
          (item) => item.id === this.loggedInUserID
        );
        this.followerCount = response.data.length;
      });

      const followingPath =
        this.backendPath + "/usuario/" + this.id + "/following";
      axios.get(followingPath).then((response) => {
        this.followingCount = response.data.length;
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
          this.getFollowers();
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
          this.getFollowers();
        })
        .catch((error) => {
          console.log(error.message);
        });
    },
  },
  mounted() {
    window.addEventListener("click", this.closeDropdown);
    this.getPublication();
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
      this.getUserInfo();
    }
    this.getFollowers();
  },
};
</script>

<style scoped>
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
