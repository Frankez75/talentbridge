from flask import Blueprint, jsonify, request, session, render_template, redirect, url_for
from pkg.models import db, Follow, TbArtist, TbPatron, Notification
from datetime import datetime

social = Blueprint('social', __name__, url_prefix='/social')

def notify(recipient_type, recipient_id, message, link=None):
    """Helper to create a notification"""
    n = Notification(
        recipient_type=recipient_type,
        recipient_id=recipient_id,
        message=message,
        link=link,
        created_at=datetime.utcnow()
    )
    db.session.add(n)
    db.session.commit()

@social.route('/follow/<int:artist_id>', methods=['POST'])
def follow_artist(artist_id):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'You must be logged in to follow artists.'}), 401
        
    follower_id = session.get('user_id')
    follower_type = session.get('user_type')
    
    # Can't follow yourself
    if follower_type == 'artist' and follower_id == artist_id:
        return jsonify({'status': 'error', 'message': 'You cannot follow yourself.'}), 400
        
    artist = db.session.query(TbArtist).get(artist_id)
    if not artist:
        return jsonify({'status': 'error', 'message': 'Artist not found.'}), 404
        
    # Check if already following
    existing = db.session.query(Follow).filter_by(
        follower_type=follower_type,
        follower_id=follower_id,
        followed_artist_id=artist_id
    ).first()
    
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'status': 'success', 'action': 'unfollowed'})
    else:
        new_follow = Follow(
            follower_type=follower_type,
            follower_id=follower_id,
            followed_artist_id=artist_id,
            created_at=datetime.utcnow()
        )
        db.session.add(new_follow)
        
        # Notify the artist
        follower_name = session.get('user_name')
        notify(
            recipient_type='artist',
            recipient_id=artist_id,
            message=f"{follower_name} started following you!",
            link=url_for('social.follower_list') if follower_type == 'artist' else None
        )
        
        return jsonify({'status': 'success', 'action': 'followed'})

@social.route('/notifications')
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    
    notifs = db.session.query(Notification).filter_by(
        recipient_type=user_type,
        recipient_id=user_id
    ).order_by(Notification.created_at.desc()).all()
    
    # Mark as read
    for n in notifs:
        if not n.is_read:
            n.is_read = True
    db.session.commit()
    
    return render_template('social/notifications.html', notifications=notifs)

@social.route('/api/notifications/unread_count')
def unread_count():
    if 'user_id' not in session:
        return jsonify({'count': 0})
        
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    
    count = db.session.query(Notification).filter_by(
        recipient_type=user_type,
        recipient_id=user_id,
        is_read=False
    ).count()
    
    return jsonify({'count': count})

@social.route('/api/feeds')
def get_feeds():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'})
        
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    
    from pkg.models import TbArt, OrderPurchaseDetail
    from sqlalchemy import func
    
    # 1. Followed Artists Feed (Recent art from followed artists)
    followed_feed = []
    if user_type:
        followed_artists = db.session.query(Follow.followed_artist_id).filter_by(
            follower_type=user_type, follower_id=user_id
        ).subquery()
        
        recent_followed_arts = db.session.query(TbArt).filter(
            TbArt.artist_art_id.in_(followed_artists),
            TbArt.artwork_status == 'available'
        ).order_by(TbArt.art_date.desc()).limit(10).all()
        
        for art in recent_followed_arts:
            followed_feed.append({
                'id': art.art_id,
                'title': art.art_title,
                'artist': f"{art.artist.artist_fname} {art.artist.artist_lname}" if art.artist else "Unknown",
                'price': float(art.art_price) if art.art_price else 0.0,
                'image': art.art_image,
                'date': art.art_date.strftime("%b %d, %Y") if art.art_date else ""
            })
            
    # 2. Popular Arts Feed (Most purchased)
    popular_arts = db.session.query(
        TbArt, 
        func.count(OrderPurchaseDetail.purchase_id).label('purchase_count')
    ).outerjoin(OrderPurchaseDetail, TbArt.art_id == OrderPurchaseDetail.art_item_id)\
     .filter(TbArt.artwork_status == 'available')\
     .group_by(TbArt.art_id)\
     .order_by(db.text('purchase_count DESC'))\
     .limit(10).all()
     
    popular_feed = []
    for art, count in popular_arts:
        popular_feed.append({
            'id': art.art_id,
            'title': art.art_title,
            'artist': f"{art.artist.artist_fname} {art.artist.artist_lname}" if art.artist else "Unknown",
            'price': float(art.art_price) if art.art_price else 0.0,
            'image': art.art_image,
            'purchases': count
        })
        
    return jsonify({
        'status': 'success',
        'followed_feed': followed_feed,
        'popular_feed': popular_feed
    })

# ─────────────────────────────────────────
# COMMUNITIES & GROUPS
# ─────────────────────────────────────────

@social.route('/communities')
def communities_list():
    from pkg.models import CommunityGroup, GroupMember
    
    # Get all communities
    communities = db.session.query(CommunityGroup).all()
    
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    
    user_memberships = []
    if user_id:
        memberships = db.session.query(GroupMember.group_id).filter_by(
            member_type=user_type,
            member_id=user_id
        ).all()
        user_memberships = [m[0] for m in memberships]
        
    return render_template('social/communities.html', communities=communities, user_memberships=user_memberships)

@social.route('/community/<int:group_id>')
def community_detail(group_id):
    from pkg.models import CommunityGroup, ForumPost, GroupMember
    
    group = db.session.query(CommunityGroup).get_or_404(group_id)
    posts = db.session.query(ForumPost).filter_by(group_id=group_id).order_by(ForumPost.created_at.desc()).all()
    
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    
    is_member = False
    if user_id:
        is_member = db.session.query(GroupMember).filter_by(
            group_id=group_id,
            member_type=user_type,
            member_id=user_id
        ).first() is not None
        
    return render_template('social/community_detail.html', group=group, posts=posts, is_member=is_member)

@social.route('/community/<int:group_id>/join', methods=['POST'])
def join_community(group_id):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
        
    from pkg.models import CommunityGroup, GroupMember
    
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    
    # Check if already member
    member = db.session.query(GroupMember).filter_by(
        group_id=group_id,
        member_type=user_type,
        member_id=user_id
    ).first()
    
    if member:
        # Leave
        db.session.delete(member)
        db.session.commit()
        return jsonify({'status': 'success', 'action': 'left'})
    else:
        # Join
        new_member = GroupMember(
            group_id=group_id,
            member_type=user_type,
            member_id=user_id,
            joined_at=datetime.utcnow()
        )
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'status': 'success', 'action': 'joined'})

@social.route('/community/<int:group_id>/post', methods=['POST'])
def create_post(group_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    content = request.form.get('content')
    if not content:
        return redirect(url_for('social.community_detail', group_id=group_id))
        
    from pkg.models import ForumPost, GroupMember
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    
    # Verify membership
    is_member = db.session.query(GroupMember).filter_by(
        group_id=group_id,
        member_type=user_type,
        member_id=user_id
    ).first()
    
    if not is_member:
        return redirect(url_for('social.community_detail', group_id=group_id))
        
    new_post = ForumPost(
        group_id=group_id,
        author_type=user_type,
        author_id=user_id,
        content=content,
        created_at=datetime.utcnow()
    )
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(url_for('social.community_detail', group_id=group_id))
