import React, { useState, useEffect } from 'react'
import EventDropdown from './eventDropdown.js'
import Poster from './poster.js'
// import Download from './download.js'
const Posters = () => {
  const [regions, setRegions] = useState([])
  // const [templates, setTemplates] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const [posterRegion, setPosterRegion] = useState('')
  const [posterFormat, setPosterFormat] = useState('png')

  useEffect(() => {
    if (regions.length == 0) {
      fetch('https://clear.codeday.org/api/regions/')
        .then(res => res.json())
        .then(
          result => {
            setLoading(true)
            setRegions(result.filter(region => region.current_event != null))
          },
          error => {
            setLoading(true)
            setError(error)
          }
        )
    }
  })
  const templates = [
    'ArtistsMeetBlack',
    'ArtistsMeetLine',
    'ArtistsMeetRed',
    'Blobs',
    'Outrun',
    'Scribble',
    'Space',
    'lastChance'
  ]
  return (
    <>
      <h1>CodeDay Poster Generator</h1>
      City webname: <EventDropdown
        error={error}
        isLoading={loading}
        regions={regions}
        setRegion={setPosterRegion}
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
          />
        ))}
      </div>
    </>
  )
}
export default Posters
