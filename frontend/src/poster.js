import React from 'react'

const Poster = props => {
  const regionIds = props.regions.map(region => region.webname)

  if (regionIds.includes(props.posterRegion)) {
    return (
      <div className='poster'>
        <a
          href={`api/generate/${props.posterRegion}/${props.posterTemplate}/pdf`}
          target='_self'
          download={`${props.posterRegion}_${props.posterTemplate}`}
        >
          <img
            src={`api/generate/${props.posterRegion}/${props.posterTemplate}/${props.posterFormat}`}
          />
        </a>
      </div>
    )
  } else {
    return null
  }
}

export default Poster
