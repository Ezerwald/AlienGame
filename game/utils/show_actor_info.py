from ..interfaces import IActor

def show_actor_info(actor: IActor) -> None:
    print(f"Name: {actor.name}")
    print(f"Room: {actor.room.name if actor.room else 'None'}")
    print(f"Base Initiative: {actor.base_initiative}")
    print(f"Initiative Modifier: {actor.initiative_modifier}")
    print(f"Role: {actor.actor_type.name}")
    
    if hasattr(actor, 'biomass'):
        print(f"Biomass: {actor.biomass}")
    
    if hasattr(actor, 'health'):
        print(f"Health: {getattr(actor, 'health', 'N/A')}")
    
    print("-----")