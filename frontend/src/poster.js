import React from 'react'

const Poster = props => {
  const regionIds = props.regions.map(region => region.webname)

  if (regionIds.includes(props.posterRegion)) {
    return (
      <div className='poster'>
        <a
          href={`api/generate/${props.posterRegion}/${props.posterTemplate}/pdf?promo=${encodeURIComponent(props.posterPromo)}`}
          target="_self"
          download={`${props.posterRegion}_${props.posterTemplate}${props.posterPromo ? '_'+props.posterPromo : ''}.pdf`}
        >
          <img
            src={`/preview/${props.posterTemplate}.png`}
            style={{width: '300px'}}
          />
        </a>
        <br />
        <a
          href={`api/generate/${props.posterRegion}/${props.posterTemplate}/png?promo=${encodeURIComponent(props.posterPromo)}`}
          target="_blank"
        >png</a>,
        <a
          href={`api/generate/${props.posterRegion}/${props.posterTemplate}/pdf?promo=${encodeURIComponent(props.posterPromo)}`}
          target="_self"
          download={`${props.posterRegion}_${props.posterTemplate}${props.posterPromo ? '_'+props.posterPromo : ''}.pdf`}
        >pdf</a>
      </div>
    )
  } else {
    return null
  }
}

export default Poster
