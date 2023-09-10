document.addEventListener('DOMContentLoaded', () => {
    anime({
        targets: '.shop-now',
        translateX: [-300, 0],
        duration: 1500,
        easing: 'easeOutCubic',
        delay: 200,
        opacity: [0, 1]
    })

    new Waypoint({
        element: document.getElementById('our_mission_img'),
        handler: function () {
            anime({
                targets: '#our_mission_img',
                duration: 1500,
                scale: [0.5, 1],
                opacity: [0, 1],
                delay: 300,
            })
        },
        offset: '100%'
    })

    new Waypoint({
        element: document.getElementById('our_mission'),
        handler: function () {
            anime({
                targets: '#our_mission',
                translateX: [300, 0],
                duration: 1500,
                easing: 'easeOutCubic',
                opacity: [0, 1],
                delay: 300,
            })
        },
        offset: '100%'
    })

    new Waypoint({
        element: document.getElementById('our_product'),
        handler: function () {
            anime({
                targets: '#our_product',
                translateX: [-300, 0],
                duration: 1500,
                easing: 'easeOutCubic',
                opacity: [0, 1],
                delay: 300,
            })
        },
        offset: '100%'
    })

    new Waypoint({
        element: document.getElementById('our_product_img'),
        handler: function () {
            anime({
                targets: '#our_product_img',
                translateX: [300, 0],
                duration: 1500,
                easing: 'easeOutCubic',
                opacity: [0, 1],
                delay: 300,
            })
        },
        offset: '100%'
    })

    new Waypoint({
        element: document.getElementById('expert_consultation'),
        handler: function () {
            anime({
                targets: '#expert_consultation',
                translateX: [-600, 0],
                duration: 1500,
                easing: 'easeOutCubic',
                opacity: [0, 1],
                delay: 300,
            })
        },
        offset: '100%'
    })

    new Waypoint({
        element: document.getElementById('forum'),
        handler: function () {
            anime({
                targets: '#forum',
                translateX: [600, 0],
                duration: 1500,
                easing: 'easeOutCubic',
                opacity: [0, 1],
                delay: 300,
            })
        },
        offset: '100%'
    })

    new Waypoint({
        element: document.getElementById('online_shopping'),
        handler: function () {
            anime({
                targets: '#online_shopping',
                translateX: [-600, 0],
                duration: 1500,
                easing: 'easeOutCubic',
                opacity: [0, 1],
                delay: 300,
            })
        },
        offset: '100%'
    })

    new Waypoint({
        element: document.getElementById('sharing'),
        handler: function () {
            anime({
                targets: '#sharing',
                translateX: [600, 0],
                duration: 1500,
                easing: 'easeOutCubic',
                opacity: [0, 1],
                delay: 300,
            })
        },
        offset: '100%'
    })

    new Waypoint({
        element: document.getElementById('footer'),
        handler: function () {
            anime({
                targets: '.footer-div-from-up',
                translateY: [-300, 0],
                duration: 1500,
                easing: 'easeOutCubic',
                opacity: [0, 1],
                delay: 300,
            })
            anime({
                targets: '.footer-div-from-down',
                translateY: [300, 0],
                duration: 1500,
                easing: 'easeOutCubic',
                opacity: [0, 1],
                delay: 300,
            })
        },
        offset: '100%'
    })

    new Waypoint({
        element: document.getElementById('footer_copyright'),
        handler: function () {
            anime({
                targets: '.footer-copyright-from-left',
                translateX: [-300, 0],
                duration: 1500,
                easing: 'easeOutCubic',
                opacity: [0, 1],
                delay: 300,
            })
            anime({
                targets: '.footer-copyright-from-right',
                translateX: [300, 0],
                duration: 1500,
                easing: 'easeOutCubic',
                opacity: [0, 1],
                delay: 300,
            })
        },
        offset: '100%'
    })
})
