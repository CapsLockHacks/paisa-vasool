<template>
  <div class="create-split">
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-text-field v-model="name" label="Name" required :rules="nameRules"></v-text-field>
      <v-text-field v-model="amount" label="Amount" value="10.00" prefix="₹" required :rules="amountRules"></v-text-field>

      <v-row>
        <v-col cols="24">
          <v-checkbox v-model="recurring" label="Recurring?"></v-checkbox>
        </v-col>
        <v-col cols="24">
          <v-select v-if="recurring" v-model="frequency" :items="['Weekly', 'Monthly', 'Yearly']" label="Frequency"></v-select>
        </v-col>
      </v-row>

      <div class="header-section">
        <v-row>
          <v-col cols="24">
            <div class="title">Contacts</div>
          </v-col>
          <v-col cols="24" class="text-right">
            <v-btn icon>
              <v-icon @click="newContact">mdi-plus</v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <v-divider></v-divider>
      </div>

      <div v-for="(c, $index) in contacts" :key="$index">
        <v-row>
          <v-col cols="8">
            <v-autocomplete label="Contact" v-model="c.contact_id"
              :items="contactsFetched" item-text="name" item-value="id"></v-autocomplete>
          </v-col>
          <v-col cols="4">
            <v-text-field v-model="c.amount" label="Amount" required :rules="amountRules"></v-text-field>
          </v-col>
        </v-row>
      </div>

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
        <v-card-text>Error creating split, try again.</v-card-text>
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
          <v-btn color="green darken-1" text @click="gotoSplits">Ok</v-btn>
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
      name: '',
      amount: null,
      recurring: false,
      contacts: [],
      contactsFetched: [],
      frequency: 'Monthly',
      showDialog: false,
      isCreating: false,
      isCreateError: false,
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length <= 10) || 'Name must be less than 20 characters'
      ],
      amountRules: [
        v => !!v || 'Amount is required',
        v => /(\d+(\.\d+)?)/.test(v) || 'Invalid amount'
      ]
    }
  },
  mounted () {
    this.newContact()
    this.fetchContacts()
  },
  methods: {
    fetchContacts () {
      axios.get('/api/contacts/').then((resp) => {
        this.contactsFetched = resp.data
      }).catch((_) => {}).finally(() => {})
    },
    submit () {
      if (this.$refs.form.validate()) {
        this.showDialog = true
        this.isCreating = true
        axios.post('/api/splits/create/', {
          subscription: this.name,
          frequency: this.frequency.toLowerCase(),
          splits: this.contacts
        }).then((_) => {
          // console.log('posted successfully')
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
    onContactChange (c, newVal) {
      c.values = newVal
    },
    newContact () {
      let amount = 0
      if (this.amount) {
        try {
          amount = parseFloat((parseFloat(this.amount) / (this.contacts.length + 1)).toFixed(2))
        } catch (err) {
        }
      }

      for (let c of this.contacts) {
        c.amount = amount || null
      }

      this.contacts.push({
        contact_id: null,
        amount: amount || null
      })
    },
    gotoSplits () {
      this.$router.push({
        name: 'splits'
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
