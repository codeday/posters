import React, { useState, useEffect } from 'react'
import EventDropdown from './eventDropdown'
import Poster from './poster'
import PromoInfo from './promoInfo'
import { gql } from 'graphql-tag';
import { apiFetch } from '@codeday/topo/utils'

// import Download from './download.js'
const Posters = () => {
  const [regions, setRegions] = useState([])
  const [templates, setTemplates] = useState([])
  // const [templates, setTemplates] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const [posterPromo, setPosterPromo] = useState('')
  const [posterPromoFor, setPosterPromoFor] = useState('')
  const [posterRegion, setPosterRegion] = useState('')
  const [posterFormat, setPosterFormat] = useState('svg')
  const query = gql`
    {
      clear {
        events {
          name
          contentfulWebname
        }
      }
    }
  `

  useEffect(() => {
    if (regions.length === 0 && !error) {
      apiFetch(query).then(result => {
        if (result) {
          setLoading(true)
          setRegions(result.clear.events.map(item => ({ webname: item.contentfulWebname, name: item.name })))
        }
      }).catch((error) => {
        console.error(error);
        setLoading(true)
        setError(error)
      });
    }
    if (templates.length === 0) {
      fetch('/api/list-templates')
        .then(res => res.json())
        .then(
          result => {
            setLoading(true)
            setTemplates(result)
          },
          error => {
            setLoading(true)
            setError(error)
          }
        )
    }
  });

  return (
    <>
      <EventDropdown
        error={error}
        isLoading={loading}
        regions={regions}
        setRegion={setPosterRegion}
      />
      <PromoInfo
        promo={posterPromo}
        promoFor={posterPromoFor}
        setPromo={setPosterPromo}
        setPromoFor={setPosterPromoFor}
      />
      {/* <Download regions={regions} posterRegion={posterRegion} /> */}
      <div className='posterGallery'>
        {templates.map((template) => (
          <Poster
            key={template}
            regions={regions}
            posterRegion={posterRegion}
            posterTemplate={template}
            posterFormat={posterFormat}
            posterPromo={posterPromo}
            posterPromoFor={posterPromoFor}
          />
        ))}
      </div>
    </>
  )
}
export default Posters
