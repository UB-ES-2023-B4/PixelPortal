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
            <h1 class="title">Post Image</h1>
            <h3 class="title">Preview:</h3>
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
                data-cy="image-upload-input"
                @change="imageInputChanged"
              />
            </div>
            <div class="form-input">
              <h4 class="title">Title</h4>
              <input
                type="text"
                placeholder="Title"
                class="image-title-input"
                v-model="imageTitle"
                data-cy="upload-title"
                @keyup="isPublishButtonEnabled"
              />
            </div>
            <div class="form-input">
              <h4 class="title">Description</h4>
              <textarea
                type="text"
                placeholder="Description"
                class="image-description-input"
                v-model="imageDescription"
                data-cy="upload-description"
                @keyup="isPublishButtonEnabled"
              />
            </div>
            <div class="form-input">
              <div class="tags-wrapper">
                <div class="tags-title">
                  <img class="tags-icon" src="../assets/tags-fill.svg" alt="" />
                  <h4 class="title">Tags</h4>
                </div>
                <div class="tags-content">
                  <p>Press enter or add a coma after each tag</p>
                  <div class="tag-box">
                    <ul class="tags-list">
                      <li
                        v-for="tag in tags"
                        :key="tag"
                        @click="removeTag(tag)"
                      >
                        {{ tag }}
                        <i class="uit uit-multiply"></i>
                      </li>
                      <input
                        class="image-tags-input"
                        type="text"
                        v-model="tag"
                        data-cy="upload-tags-input"
                        @keyup="addTag"
                      />
                    </ul>
                  </div>
                </div>
                <div class="tags-details">
                  <p>
                    <span>{{ this.remainingTags }}</span> tags are remaining
                  </p>
                  <button class="tags-button" @click="clearTags">
                    Remove All
                  </button>
                </div>
              </div>
            </div>
            <div class="form-button">
              <button
                type="button"
                class="popup-button"
                data-cy="upload-close-button"
                @click="closeComponent"
              >
                Close
              </button>
              <button
                type="button"
                @click="postImage"
                :disabled="!publishButtonEnabled"
                class="popup-button"
                data-cy="upload-publish-button"
                :class="{ 'disabled-button': !publishButtonEnabled }"
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
      defaultImagePath: require("@/assets/image_preview.png"),
      postImagePath: require(`@/assets/image_preview.png`),
      postImageExtension: "",
      imageTitle: "",
      imageDescription: "",
      imageID: "",
      publishButtonEnabled: false,
      tags: [],
      tag: "",
      maxTags: 10,
      remainingTags: 10,
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
    countTags() {
      this.remainingTags = this.maxTags - this.tags.length;
    },
    addTag(event) {
      if (event.key === "Enter" && this.remainingTags > 0) {
        this.tag = this.tag.replace(/\s+/g, " ").toLowerCase();
        if (this.tag.length > 1 && !this.tags.includes(this.tag)) {
          let splitTags = this.tag.split(",");
          if (splitTags.length + this.tags.length > this.maxTags) {
            alert("Too many tags at once");
          } else {
            splitTags.filter((value, index, self) => {
              return self.indexOf(value) === index;
            });
            splitTags.forEach((tag) => {
              if (!this.tags.includes(tag)) {
                this.tags.push(tag);
              }
            });
            this.tag = "";
          }
        }
      } else if (event.key === "Enter" && this.remainingTags <= 0) {
        alert("Max tags reached");
      }
      this.countTags();
    },
    removeTag(tag) {
      this.tags = this.tags.filter((t) => t !== tag);
      this.countTags();
    },
    clearTags() {
      this.tags = [];
      this.countTags();
    },
    imageInputChanged() {
      const imageInput = this.$refs.imageInput;

      // Check if the user canceled the file selection
      if (!imageInput.files.length) {
        this.postImagePath = this.defaultImagePath;
        return;
      }

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
    resetValues() {
      const imageInput = this.$refs.imageInput;
      this.postImagePath = this.defaultImagePath;
      imageInput.value = "";
      this.imageTitle = "";
      this.imageDescription = "";
      this.postImageExtension = "";
      this.imageID = "";
      this.publishButtonEnabled = false;
    },
    closeComponent() {
      this.resetValues();

      this.$emit("close", { hasPosted: false });
    },
    postImage() {
      this.isPublishButtonEnabled();
      if (this.publishButtonEnabled) {
        const imageInput = this.$refs.imageInput;
        var imageToUpload = imageInput.files[0];
        this.imageID = this.uuidv4();
        const imagePostedRef = ref(
          storage,
          "postedImages/" + this.imageID + "." + this.postImageExtension
        );
        console.log("Posting...");
        uploadBytes(imagePostedRef, imageToUpload).then(() => {
          this.$emit("close", {
            hasPosted: true,
            imageID: this.imageID + "." + this.postImageExtension,
            imageTitle: this.imageTitle,
            imageDescription: this.imageDescription,
            username: this.username,
            imageTags: this.tags,
          });
          this.resetValues();
        });
      }
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

.image-upload-input {
  border: none;
  padding: 10px;
  border-radius: 6px;
  cursor: pointer;
}

.image-preview-display {
  height: 10rem;
  width: 10rem;
  border-radius: 10%;
  object-fit: cover;
  background: #dfdfdf;
}

.image-title-input {
  width: 100%;
  height: 35px;
  border-radius: 6px;
}
.image-description-input {
  height: 5rem;
  resize: vertical;
  overflow-y: auto;
  padding: 5px;
  border-radius: 6px;
  width: 100%;
}
.form-button {
  margin-top: 10px;
  align-items: center;
  justify-content: center;
  display: flex;
}
.popup-button {
  background-color: rgba(20, 117, 236, 0.9);
  color: white;
  height: 45px;
  width: 8rem;
  margin: 10px;
  border-radius: 6px;
}

.popup-button.disabled-button {
  background-color: rgba(20, 117, 236, 0.5);
  pointer-events: none;
  cursor: not-allowed;
}

.popup-button:hover {
  background-color: rgba(20, 117, 236, 1);
}

.popup-button.disabled-button:hover {
  background-color: rgba(20, 117, 236, 0.5);
}

.tags-button {
  background-color: rgba(20, 117, 236, 0.9);
  color: white;
  height: 2rem;
  width: 100%;
  margin: 10px;
  border-radius: 6px;
}

.tags-icon {
  max-width: 21px;
  height: 25px;
}
.tags-title {
  display: flex;
}

.tags-wrapper .tags-content {
  margin: 10px 0;
}

.tags-wrapper :where(.tags-title, li, li i, .tags-details) {
  display: flex;
  align-items: center;
}

.tags-content ul {
  display: flex;
  padding: 7px;
  border-radius: 5px;
  border: 1px solid #a6a6a6;
}

.tags-content ul li {
  list-style: none;
  padding: 5px 8px 5px 10px;
  background: #f2f2f2;
  margin: 4px 3px;
  border: 1px solid #e3d1e1;
}

.tags-content ul li i {
  height: 20px;
  width: 20px;
  font-size: 12px;
  cursor: pointer;
  color: #808080;
  background: #dfdfdf;
  margin-left: 8px;
  border-radius: 50%;
  justify-content: center;
}
.tags-list {
  display: flex;
  flex-wrap: wrap; /* Allow the tags to wrap to new lines */
  padding: 7px;
  border-radius: 5px;
  border: 1px solid #a6a6a6;
  list-style: none;
  margin: 0;
}

.tags-content ul input {
  flex: 1;
  outline: none;
  border: none;
  padding: 5px;
  font-size: 16px;
}

.tags-wrapper .tags-details {
  justify-content: space-between;
}

.title {
  font-weight: 600;
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
