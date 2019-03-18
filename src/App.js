import React, { Component } from 'react'
import Select from 'react-select'
import ProgressBar from 'react-progress-bar-plus'

import { getShopNames, getKeyTerms } from './lib/api'
import KeyTermsListing from './components/KeyTermsListing'

import './App.css'
import 'react-progress-bar-plus/lib/progress-bar.css'

class App extends Component {
  state = {
    isLoading: false,
    shopNames: [],
    selections: [],
    progressAutoIncrement: false,
    progressPercent: -1,
    progressIntervalTime: 20
  }

  componentDidMount () {
    this.startProgress()
    getShopNames().then(shopNames => this.stopProgress({ shopNames }))
  }

  startProgress = state => {
    this.setState({
      progressPercent: 10,
      progressAutoIncrement: true,
      isLoading: true,
      ...state
    })
  }

  stopProgress = state => {
    this.setState({
      progressPercent: -1,
      progressAutoIncrement: false,
      isLoading: false,
      ...state
    })
  }

  handleShopSelection = newSelection => {
    this.startProgress()

    const selectedIdx = this.state.shopNames.indexOf(newSelection)
    const shopNames = [
      ...this.state.shopNames.slice(0, selectedIdx),
      ...this.state.shopNames.slice(selectedIdx + 1)
    ]

    // Poll the server for key terms for the selected shop
    getKeyTerms(newSelection.label).then(({ shop_name, key_terms }) => {
      const selectedShop = { shop: shop_name, terms: key_terms.join(', ') }
      const selections = [selectedShop, ...this.state.selections]
      this.stopProgress({ selections, shopNames })
    })
  }

  render () {
    return (
      <div className='App'>
        <h1>Etsy shop text analysis</h1>
        <p>
          Select a shop to see the most important words found in its listing
          titles and descriptions.
        </p>

        <ProgressBar
          color='#77b6ff'
          spinner='left'
          onTop={true}
          autoIncrement={this.state.progressAutoIncrement}
          percent={this.state.progressPercent}
          intervalTime={this.state.progressIntervalTime}
        />

        <Select
          options={this.state.shopNames}
          onChange={this.handleShopSelection}
          isLoading={this.state.isLoading}
          placeholder='Select a shop...'
        />

        <KeyTermsListing selections={this.state.selections} />
      </div>
    )
  }
}

export default App
