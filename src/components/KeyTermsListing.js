import React from 'react'

import './KeyTermsListing.css'

const KeyTermList = ({ shop, terms }) => (
  <div className='KeyTermList'>
    <div>
      <strong>
        <a
          href={`https://etsy.com/shop/${shop}`}
          target='_blank'
          rel='noopener noreferrer'
        >
          {shop}
        </a>
      </strong>
    </div>
    <div>{terms.length ? terms : 'Not enough listings'}</div>
  </div>
)

const KeyTermsListing = ({ selections }) => (
  <div className='KeyTermsListing'>
    {selections.map((selection, i) => (
      <KeyTermList key={i} {...selection} />
    ))}
  </div>
)

export default KeyTermsListing
