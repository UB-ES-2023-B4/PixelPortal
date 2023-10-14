<template>
  <transition name="fade">
    <div class="popup" v-show="open">
      <transition name="drop-in">
        <div class="popup-inner" v-show="open">
          <div class="popup-content">
            <h1>Post Image</h1>
            <h3>Preview:</h3>
            <div class="form-input">
              <img
                :src="postImagePath"
                alt=""
                class="image-preview-display"
                ref="imagePreviewDisplay"
              />
            </div>
            <div class="form-input">
              <input
                type="file"
                class="image-upload-input"
                ref="imageInput"
                accept="image/png,image/jpeg"
                @change="imageInputChanged"
              />
            </div>
            <div class="form-input">
              <input
                type="text"
                placeholder="Title"
                class="image-title-input"
                v-model="imageTitle"
                @keyup="isPublishButtonEnabled"
              />
            </div>
            <div class="form-input">
              <textarea
                type="text"
                placeholder="Description"
                class="image-description-input"
                v-model="imageDescription"
                @keyup="isPublishButtonEnabled"
              />
            </div>
            <div class="form-button">
              <button type="button" @click="closeComponent">Close</button>
              <button
                type="button"
                @click="postImage"
                :disabled="!publishButtonEnabled"
              >
                Publish
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>

<script>
import { ref, uploadBytes } from "firebase/storage";
import { storage } from "@/firebase";
export default {
  name: "UploadImagePopup",
  props: {
    open: {
      type: Boolean,
      required: true,
    },
    username: {
      type: String,
      required: true,
    },
    token: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      defaultImagePath: require("@/assets/default_PFP.png"),
      postImagePath: require(`@/assets/default_PFP.png`),
      postImageExtension: "",
      imageTitle: "",
      imageDescription: "",
      imageID: "",
      publishButtonEnabled: false,
    };
  },
  methods: {
    //Creates a randomly generated UUID to uploade image to firebase
    uuidv4() {
      return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, (c) =>
        (
          c ^
          (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
        ).toString(16)
      );
    },
    imageInputChanged() {
      const imageInput = this.$refs.imageInput;
      this.postImageExtension = imageInput.files[0].name.split(".").pop();
      this.postImagePath = URL.createObjectURL(imageInput.files[0]);
      this.isPublishButtonEnabled();
    },
    isPublishButtonEnabled() {
      const imageInput = this.$refs.imageInput;
      this.publishButtonEnabled =
        imageInput &&
        imageInput.files &&
        imageInput.files.length > 0 &&
        this.imageTitle.trim() !== "" &&
        this.imageDescription.trim() !== "";
    },
    closeComponent() {
      const imageInput = this.$refs.imageInput;
      this.postImagePath = this.defaultImagePath;
      imageInput.value = "";
      this.imageTitle = "";
      this.imageDescription = "";
      this.postImageExtension = "";
      this.imageID = "";
      this.publishButtonEnabled = false;

      this.$emit("close", { hasPosted: false });
    },
    postImage() {
      this.imageID = this.uuidv4();
      const imagePostedRef = ref(
        storage,
        "postedImages/" + this.imageID + "." + this.postImageExtension
      );
      console.log("Posting...");
      uploadBytes(imagePostedRef, this.postImagePath).then(() => {
        console.log("UPLOADED BLOB OR FILE!");
        this.$emit("close", {
          hasPosted: true,
          imageID: this.imageID + "." + this.postImageExtension,
          imageTitle: this.imageTitle,
          imageDescription: this.imageDescription,
        });
      });
    },
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
  max-width: 500px;
  margin: 2rem auto;
}

.popup-content {
  position: relative;
  background-color: white;
  border: 1px solid rgba(0, 0, 0, 0.3);
  background-clip: padding-box;
  border-radius: 0.3rem;
  padding: 1rem;
}

.form-input {
  margin-bottom: 10px; /* Adjust the margin as needed to separate the elements */
}

.image-preview-display {
  height: 300px;
  width: 300px;
  border-radius: 10%;
  object-fit: cover;
  background: #dfdfdf;
}

.image-title-input {
  width: 100%;
}
.image-description-input {
  height: 100px;
  resize: vertical;
  overflow-y: auto;
  padding: 5px;
  width: 100%;
}
.form-button {
  margin-top: 10px; /* Adjust the margin as needed to separate the elements */
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
