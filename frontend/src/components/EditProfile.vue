<template>
    <div class="container py-5">

        <div class="row align-items-center">
            <div class="col-lg-6 mx-auto">
                <div class="card mb-4 mx-auto">
                    <div class="card-body text-center">
                        <img :src="profilePicture" class="rounded-circle img-fluid" style="width: 150px; height: 150px;">
                    </div>
                    <div class="form-input mx-auto">
                        <input type="file" class="image-upload-input" ref="imageInput" accept="image/png,image/jpeg"
                            @change="imageInputChanged" />
                    </div>
                </div>
            </div>
        </div>
        <div class="row align-items-center">
            <div class="col-lg-6 mx-auto">
                <div class="card mb-4">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-sm-3">
                                <p class="mb-0">Name</p>
                            </div>
                            <div class="col-sm-9">
                                <input type="text" id="name" v-model="username" class="form-control"
                                    placeholder="{{username}}">
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-sm-3">
                                <p class="mb-0">Email</p>
                            </div>
                            <div class="col-sm-9">
                                <p class="text-muted mb-0">{{ email }}</p>
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-sm-3">
                                <p class="mb-0">Description</p>
                            </div>
                            <div class="col-sm-9">
                                <textarea id="description" v-model="description" class="form-control"
                                    placeholder="{{description}}"></textarea>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="d-flex justify-content-center mb-2">
                <button type="button" class="btn btn-primary">Save</button>
                <button type="button" class="btn btn-outline-primary ms-1" @click="goBack">Cancel</button>
            </div>
        </div>
    </div>
</template>
  
<script>
import { ref } from "vue";
import { storage } from "@/firebase";
import { ref as firebaseRef, getDownloadURL } from "firebase/storage";
import axios from "axios";

export default {
    name: "PostZoom",
    setup() {
        const showUploadImageForm = ref(false);
        return { showUploadImageForm };
    },
    data() {
        return {
            id: this.$route.params.id,
            username: "",
            token: this.$route.query.token,
            description: "",
            profilePicture: "",
            postImageExtension: "",
            leftSidebarMinimized: false,
            musicPlayerVisible: false,
            timerDisplayVisible: false,
            directMessagingVisible: false,
            imageList: [],
            currentUserImages: [],
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
        goBack() {
            history.back();
        },
        imageInputChanged() {
            const imageInput = this.$refs.imageInput;

            // Check if the user canceled the file selection
            if (!imageInput.files.length) {
                this.profilePicture = this.defaultImagePath;
                return;
            }

            this.postImageExtension = imageInput.files[0].name.split(".").pop();
            this.profilePicture = URL.createObjectURL(imageInput.files[0]);
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
</style>   