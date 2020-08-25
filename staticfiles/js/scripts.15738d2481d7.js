(function( win ) {

  'use strict';

  /*

      Disable rollovers on touch devices

  */

  function detectTouchDevice()
  {
    if ( ( 'ontouchstart' in window ) || ( navigator.MaxTouchPoints > 0 ) || ( navigator.msMaxTouchPoints > 0 ) ) {
      document.body.classList.add( 'touch' );
    }
  }

  /*

      Compact navigation upon scrolling

  */

  function enableCompactNav()
  {
    window.onscroll = function()
    {
      var header = document.querySelector( 'header' );
      if ( document.documentElement.scrollTop > 56 ) {
        header.classList.add( 'compact' );
      } else {
        header.classList.remove( 'compact' );
      }
    }
  }

  /*

      Settings dropdowns

  */

  function enableSettingsDropdown()
  {
    var settingsDD = document.querySelectorAll( '.nav-dropdown' );
    settingsDD.forEach( function( dd ){
      dd.querySelector( 'div:first-child' ).addEventListener( 'click', function(){
        this.parentElement.querySelector( '.nav-dropdown-options' ).classList.add( 'visible' );
      });
      dd.addEventListener( 'mouseleave', function(){
        this.querySelector( '.nav-dropdown-options' ).classList.remove( 'visible' );
      });
    });
    document.querySelectorAll( '.nav-dropdown-options > div' ).forEach( function( o ){
      o.addEventListener( 'click', function(){
        this.parentElement.classList.remove( 'visible' );
      })
    });
  }

  /*

      Openable Trees

  */

  function enableTrees()
  {
    var treeBtns = document.querySelectorAll( '.btn-tree' );
    treeBtns.forEach( function( btn ){
      btn.addEventListener( 'click', function(){
        if ( !this.classList.contains( 'btn-tree-open' ) ) {
          var item = this.parentElement.querySelector( '.openable' );
          item.style.setProperty( '--tree-height', item.scrollHeight + 'px' );
        }
        this.classList.toggle( 'btn-tree-open' );
      });
    });
  }

  /*

      Product Gallery

  */

  function enableProductGallery()
  {
    var thumbs = document.querySelectorAll( '.product-thumbs li' );
    thumbs.forEach( function( btn ){
      btn.addEventListener( 'click', function(){
        thumbs.forEach( function( b ){
          b.classList.remove( 'selected' );
        })
        this.classList.add( 'selected' );
      });
    });
  }

  /*

      Overlays

  */

  function checkClicksOutside( o )
  {
    if ( !o.classList.contains( 'visible' ) ) {
      window.addEventListener( 'click', function(){
        closeOverlay( o );
      });
    }
  }

  function openOverlay( e, o )
  {
    e.preventDefault();
    e.stopPropagation();
    var opened = document.querySelector( '.overlay.visible' );
    if ( opened && opened !== o ) {
      opened.classList.remove( 'visible' );
    }
    checkClicksOutside( o );
    o.classList.toggle( 'visible' );
    if ( o.id === 'overlayAuth' && o.classList.contains( 'visible' ) ) {
      document.getElementById( 'loginEmail' ).focus();
    }
  }

  function closeOverlay( o )
  {
    o.classList.remove( 'visible' );
  }

  function enableOverlays()
  {
    document.querySelectorAll( '[data-overlay]' ).forEach( function( btn ){
      btn.addEventListener( 'click', function( e ){
        openOverlay( e, document.getElementById( 'overlay' + this.dataset.overlay ) );
      });
    })
    document.querySelectorAll( '.overlay-title .btn' ).forEach( function( btn ){
      btn.addEventListener( 'click', function(){
        closeOverlay( this.parentElement.parentElement );
      });
    })
    document.querySelectorAll( '.overlay' ).forEach( function( o ){
      o.addEventListener( 'click', function( e ){
        e.stopPropagation();
      });
    })
  }

  /*

      DEMO notification

  */

  function enableNotifications()
  {
    var notif = document.querySelector( '.notification' ),
      addToCartBtn = document.getElementById( 'btnAddToCart' );
    if ( !addToCartBtn ) return;
    addToCartBtn.addEventListener( 'click', function(){
      notif.classList.add( 'visible' );
      setTimeout(function(){
        notif.classList.remove( 'visible' );
      }, 3000 );
    });
  }

  /* -------------------------- */

  detectTouchDevice();
  enableCompactNav();
  enableSettingsDropdown();
  enableTrees();
  enableProductGallery();
  enableOverlays();
  enableNotifications();

})( window );