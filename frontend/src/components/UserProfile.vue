<template>
    <div class="container py-5">

        <div class="row">
            <div class="col-lg-4">
                <div class="card mb-4">
                    <div class="card-body text-center">
                        <img :src="profilePicture" class="rounded-circle img-fluid" style="width: 150px;">
                        <h5 class="my-3">{{ username }}</h5>
                        <p class="text-muted mb-1">{{ description }}</p>
                        <div>
                            <p class="text-muted mb-1"> </p>
                        </div>
                        <div class="d-flex justify-content-center mb-2">
                            <button type="button" class="btn btn-primary">Follow</button>
                            <button type="button" class="btn btn-outline-primary ms-1">Message</button>
                        </div>
                    </div>
                </div>
                <div class="card mb-4 mb-lg-0">
                    <div class="card-body p-0">
                        <ul class="list-group list-group-flush rounded-3">
                            <li class="list-group-item d-flex justify-content-between align-items-center p-3">
                                <i class="fas fa-globe fa-lg text-warning"></i>
                                <p class="mb-0">https://mdbootstrap.com</p>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center p-3">
                                <i class="fab fa-github fa-lg" style="color: #333333;"></i>
                                <p class="mb-0">mdbootstrap</p>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center p-3">
                                <i class="fab fa-twitter fa-lg" style="color: #55acee;"></i>
                                <p class="mb-0">@mdbootstrap</p>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center p-3">
                                <i class="fab fa-instagram fa-lg" style="color: #ac2bac;"></i>
                                <p class="mb-0">mdbootstrap</p>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center p-3">
                                <i class="fab fa-facebook-f fa-lg" style="color: #3b5998;"></i>
                                <p class="mb-0">mdbootstrap</p>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-lg-8">
                <div class="image-container">
                    <div class="search-box">
                        <i class="bx bx-search"></i>
                        <input type="text" v-model="search" placeholder="Search" />
                    </div>

                    <!--
                    <div class="images">
                        <div class="image-card" v-for="img in filteredList" :key="img.id" :data-name="img.username">
                            <router-link :to="{
                                name: 'postZoom',
                                params: { id: img.id },
                                query: {
                                    token: this.token,
                                    loggedUsername: this.username,
                                },
                            }">
                                <img :src="img.image" />
                            </router-link>
                            <h6 class="image-title">{{ img.title }}</h6>
                            <h6 class="image-username">{{ img.username }}</h6>
                        </div>
                    </div>
                    -->
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import axios from "axios";
import { storage } from "@/firebase";
import { ref as firebaseRef, getDownloadURL } from "firebase/storage";

export default {
    name: "PostZoom",
    data() {
        return {
            id: this.$route.params.id,
            username: "",
            token: this.$route.query.token,
            description: "",
            profilePicture: "",
            leftSidebarMinimized: false,
            musicPlayerVisible: false,
            timerDisplayVisible: false,
            directMessagingVisible: false,
        };
    },
    computed: {
        filteredList() {
            return this.imageList.filter((img) => {
                return img.username == this.username;
            });
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
        getPublication() {
            this.imageList = [];
            const pathPublications = this.backendPath + "/publicaciones";

            axios
                .get(pathPublications)
                .then((res) => {
                    var publications = res.data.filter((publi) => {
                        return publi.id != null;
                    });
                    for (let i = 0; i < publications.length; i++) {
                        //Use publication data to recover image from Firebase and create the card
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
                                postDate: publications[i].fecha_publicacion,
                            };
                            this.imageList.push(image);
                        });
                    }
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        toggleLeftSidebar() {
            this.leftSidebarMinimized = !this.leftSidebarMinimized;
        },
        toggleMusicPlayer() {
            this.musicPlayerVisible = !this.musicPlayerVisible;
        },
        toggleTimerDisplay() {
            this.timerDisplayVisible = !this.timerDisplayVisible;
        },
        toggleDirectMessaging() {
            this.directMessagingVisible = !this.directMessagingVisible;
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
        if (typeof this.token === "undefined") {
            this.$router.push({ path: "/" });
        } else {
            this.getUserInfo();
        }
    },
};
</script>
  
<style scoped>
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
</style>   