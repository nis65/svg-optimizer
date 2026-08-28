XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"


def split_clark_name(name: str) -> tuple[str, str]:
    if name.startswith("{"):
        end = name.find("}")
        return name[1:end], name[end + 1 :]
    else:
        return "", name


# returns the tag and its namespace (to be added to the list of known namespaces)
def parse_tag(tag: str) -> (str, str):
    namespace, tag = split_clark_name(tag)
    if namespace == "":
        return tag, ""
    elif namespace == SVG_NAMESPACE:
        return tag, SVG_NAMESPACE
    elif namespace == XML_NAMESPACE:
        return f"xml:{tag}", XML_NAMESPACE
    else:
        return None, namespace


# returns the attr and its namespace (to be added to the list of known namespaces)
def parse_attr(attr: str) -> (str, str):
    namespace, attr = split_clark_name(attr)
    if namespace == "":
        return attr, ""
    elif namespace == SVG_NAMESPACE:
        raise ValueError(
            f"attribute {attr} should never have an explicit {SVG_NAMESPACE}"
        )
    elif namespace == XML_NAMESPACE:
        return f"xml:{attr}", XML_NAMESPACE
    elif namespace == XLINK_NAMESPACE:
        if attr == "href":
            return attr, None
        else:
            raise ValueError(
                f"only href supported in Namespace {XLINK_NAMESPACE}, not {attr}"
            )
