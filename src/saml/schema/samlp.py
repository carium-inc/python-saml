# -*- coding: utf-8 -*-
""" \file saml/schema/samlp.py
\brief Defines the XML data types for SAML2 in the samlp namespace.

\author Ryan Leckey (mehcode) leckey.ryan@gmail.com

\copyright Copyright © 2012 Concordus Applications, Inc.
           \n \n
           Permission is hereby granted, free of charge, to any person
           obtaining a copy of this software and associated documentation
           files (the "Software"), to deal in the Software without restriction,
           including without limitation the rights to use, copy, modify, merge,
           publish, distribute, sublicense, and/or sell copies of the Software,
           and to permit persons to whom the Software is furnished to do so,
           subject to the following conditions:
           \n \n
           The above copyright notice and this permission notice shall be
           included in all copies or substantial portions of the Software.
           \n \n
           THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
           EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
           MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
           NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
           BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
           ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
           CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
           SOFTWARE.
"""
from .. import schema
from . import saml


class Element(schema.Element):
    class Meta:
        namespace = ("samlp", "urn:oasis:names:tc:SAML:2.0:protocol")


class Message(saml.Message):
    """Specifies commonalities that are associated with all SAML protocols.
    """

    class Meta:
        namespace = Element.Meta.namespace

    ## URI reference indicating h this message has been sent.
    destination = schema.Attribute("Destination")

    ## Indicates how consent has been obtained from a principal.
    consent = schema.Attribute("Consent", 1)

    ## \todo Element <Extensions>


## \todo Element <StatusDetail>


class StatusCode(Element):
    """ Specifies a code or a set of nested codes representing the status.
    """

    class Value:
        """Enumeration of possible values."""

        ## URI prefix for the values in this enumeration.
        _PREFIX = "urn:oasis:names:tc:SAML:2.0:status:"

        ## The request succeeded.
        SUCCESS = "{}Success".format(_PREFIX)

        ## Failure due to an error on the part of the requester.
        REQUESTER = "{}Requester".format(_PREFIX)

        ## The version of the request message was incorrect.
        VERSION_MISMATCH = "{}VersionMismatch".format(_PREFIX)

        ## The provider wasn't able to successfully authenticate the principal.
        AUTHENTICATION_FAILED = "{}AuthnFailed".format(_PREFIX)

        ## Unexpected or invalid content was encountered.
        INVALID_ATTRIBUTE_NAME_OR_VALUE = "{}InvalidAttrNameOrValue".format(
            _PREFIX)

        ## The responding provider cannot support the requested name ID policy.
        INVALID_NAME_ID_POLICY = "{}InvalidNameIDPolicy".format(_PREFIX)

        ## The authentication context requirements cannot be met.
        NO_AUTHENTICATION_CONTEXT = "{}NoAuthnContext".format(_PREFIX)

        ## None of the supported identity providers are available.
        NO_AVAILABLE_IDP = "{}NoAvailableIDP".format(_PREFIX)

        ## The responding provider cannot authenticate the principal passively.
        NO_PASSIVE = "{}NoPassive".format(_PREFIX)

        ## None of the identity providers are supported by the intermediary.
        NO_SUPPORTED_IDP = "{}NoSupportedIDP".format(_PREFIX)

        ## Not able to propagate logout to all other session participants.
        PARTIAL_LOGOUT = "{}PartialLogout".format(_PREFIX)

        ## Cannot authenticate directly and not permitted to proxy the request.
        PROXY_COUNT_EXCEEDED = "{}ProxyCountExceeded".format(_PREFIX)

        ## Is able to process the request but has chosen not to respond.
        REQUEST_DENIED = "{}RequestDenied".format(_PREFIX)

        ## The SAML responder or SAML authority does not support the request.
        REQUEST_UNSUPPORTED = "{}RequestUnsupported".format(_PREFIX)

        ## Deprecated protocol version specified in the request.
        REQUEST_VERSION_DEPRECATED = "{}RequestVersionDeprecated".format(
            _PREFIX)

        ## Protocol version specified in the request message is too low.
        REQUEST_VERSION_TOO_LOW = "{}RequestVersionTooHigh".format(_PREFIX)

        ## Protocol version specified in the request message is too high.
        REQUEST_VERSION_TOO_HIGH = "{}RequestVersionTooLow".format(_PREFIX)

        ## Resource value provided in the request message is invalid.
        RESOURCE_NOT_RECOGNIZED = "{}ResourceNotRecognized".format(_PREFIX)

        ## The response message would contain more elements than able.
        TOO_MANY_RESPONSES = "{}TooManyResponses".format(_PREFIX)

        ## Attribute from an unknown attribute profile.
        UNKNOWN_ATTR_PROFILE = "{}UnknownAttrProfile".format(_PREFIX)

        ## The responder does not recognize the principal.
        UNKNOWN_PRINCIPAL = "{}UnknownPrincipal".format(_PREFIX)

        ## The SAML responder cannot properly fulfill the request.
        UNSUPPORTED_BINDING = "{}UnsupportedBinding".format(_PREFIX)

    ## The status code value.
    value = schema.Attribute("Value", required=True)

    ## \todo Element <StatusCode>


class Status(Element):
    """Represents a status returned with the response.
    """

    ## A code representing the status of the activity carried out.
    code = StatusCode(meta__min_occurs=1)

    ## A message which may be returned to give further clarification.
    message = schema.SimpleElement("StatusMessage", 1)

    # \todo Element <StatusDetail>


class StatusResponseType(Message):
    """
    Defines commonalities among all SAML protocol messages that return a
    status code along with the response.
    """

    ## A reference to the identifier of the initiating request.
    in_response_to = schema.Attribute("InResponseTo")

    ## A code representing the status of the corresponding request.
    status = Status(meta__index=1)


## \todo Element <AssertionIDRequest>
## \todo Element <SubjectQuery>
## \todo Element <AuthnQuery>
## \todo Element <RequestedAuthnContext>
## \todo Element <AttributeQuery>
## \todo Element <AuthzDecisionQuery>


class Response(StatusResponseType):
    """Used when a response consists of a list of zero or more assertions.
    """

    ## Specifies an (optionally encrypted) assertion by value.
    assertion = saml.Assertion(meta__max_occurs=None)


class AuthenticationRequest(Message):
    """To request authentication with an identity provider.
    """

    class Meta:
        name = 'AuthnRequest'

    ## Specifies the requested subject of the resulting assertion(s).
    subject = saml.Subject()

    ## \todo Element <NameIDPolicy>
    ## \todo Element <saml:Conditions>
    ## \todo Element <RequestedAuthnContext>
    ## \todo Element <Scoping>

    ## If true, the identity provider MUST authenticate.
    is_forced = schema.Attribute("ForceAuthn", 1)

    ## If true, the identity provider itself MUST NOT visibly take control.
    is_passive = schema.Attribute("IsPassive", 2)

    ## Indirectly identifies the location of where to send the response.
    assertion_consumer_service_index = schema.Attribute(
        name="AssertionConsumerServiceIndex",
        index=3)

    ## Specifies the location to which the <Response> message must be sent.
    assertion_consumer_service_url = schema.Attribute(
        name="AssertionConsumerServiceURL",
        index=4)

    ## A URI reference that identifies a SAML protocol binding to be used.
    protocol_binding = schema.Attribute(
        name="ProtocolBinding",
        index=5,
        required=True,
        default=Element.namespace[1])

    ## Indirectly identifies the SAML attributes the requester desires.
    attribute_consuming_service_index = schema.Attribute(
        name="AttributeConsumingServiceIndex",
        index=6)

    ## Specifies the human-readable name of the requester.
    provider_name = schema.Attribute(16, "ProviderName")

## \todo Element <NameIDPolicy>
## \todo Element <Scoping>
## \todo Element <IDPList>
## \todo Element <IDPEntry>
## \todo Element <ArtifactResolve>
## \todo Element <ArtifactResponse>
## \todo Element <ManageNameIDRequest>
## \todo Element <ManageNameIDResponse>
## \todo Element <LogoutRequest>
## \todo Element <LogoutResponse>
## \todo Element <NameIDMappingRequest>
## \todo Element <NameIDMappingResponse>
