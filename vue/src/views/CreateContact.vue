<template>
  <div class="create-split">
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-text-field v-model="name" label="Name" required :rules="nameRules"></v-text-field>
      <v-text-field v-model="phone" label="Phone" required :rules="phoneRules"></v-text-field>
      <v-text-field v-model="email" label="Email" :rules="emailRules"></v-text-field>

      <v-row>
        <v-col cols="2">
          &nbsp;
        </v-col>
        <v-col cols="46" class="text-right">
          <v-btn @click="submit" class="blue-grey" dark>Submit</v-btn>
        </v-col>
      </v-row>
    </v-form>

    <v-dialog v-model="showDialog" persistent max-width="290">
      <v-card v-if="isCreating" class="loader">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-card>
      <v-card v-else-if="isCreateError">
        <v-card-title class="headline">Error</v-card-title>
        <v-card-text>Error adding contact, try again.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="reset">Ok</v-btn>
        </v-card-actions>
      </v-card>
    <v-card v-else>
        <v-card-title class="headline">Success</v-card-title>
        <v-card-text>Created successfully.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="gotoContacts">Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      valid: false,
      name: null,
      phone: null,
      email: null,
      showDialog: false,
      isCreating: false,
      isCreateError: false,
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length <= 10) || 'Name must be less than 20 characters'
      ],
      phoneRules: [
        v => !!v || 'Phone is required',
        v => /[2-9]{2}\d{8}/.test(v) || 'Invalid phone'
      ],
      emailRules: [
        v => !v || /.+@.+\..+/.test(v) || 'Email must be valid'
      ]
    }
  },
  methods: {
    submit () {
      if (this.$refs.form.validate()) {
        this.showDialog = true
        this.isCreating = true
        axios.post('/api/contacts/', {
          name: this.name,
          phone: this.phone,
          email: this.email
        }).then((resp) => {
          // console.log('created successfully')
        }).catch((_) => {
          // console.log('error posting : ', err)
          this.isCreateError = true
        }).finally(() => {
          this.isCreating = false
        })
      }
    },
    reset () {
      this.isCreating = false
      this.isCreateError = false
      this.showDialog = false
    },
    gotoContacts () {
      this.$router.push({
        name: 'contacts'
      })
    }
  }
}
</script>

<style>
  .create-split {
    padding: 20px;
  }

  .sub-header {
    font-size: 14px;
    opacity: 0.6;
    margin-bottom: 10px;
  }

  .loader {
    text-align: center;
    padding: 30px;
  }
</style>
