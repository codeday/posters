import React from 'react'

const Poster = props => {
  const regionIds = props.regions.map(region => region.webname)

  if (regionIds.includes(props.posterRegion)) {
    return (
      <div className='poster'>
        <a
          href={`api/generate/${props.posterRegion}/${props.posterTemplate}/pdf`}
          target="_blank"
          download={`${props.posterRegion}_${props.posterTemplate}`}
        >
          <img
            src={`api/generate/${props.posterRegion}/${props.posterTemplate}/${props.posterFormat}`}
            style={{width: '300px'}}
          />
        </a>
        <br />
        <a
          href={`api/generate/${props.posterRegion}/${props.posterTemplate}/png`}
          target="_blank"
        >png</a>,
        <a
          href={`api/generate/${props.posterRegion}/${props.posterTemplate}/pdf`}
          target="_blank"
        >pdf</a>
      </div>
    )
  } else {
    return null
  }
}

export default Poster
