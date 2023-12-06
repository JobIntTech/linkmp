{{/* Generate application fullname with qa identifier */}}
{{- define "application.fullname" -}}
{{- if eq .Release.Namespace "qa" -}}
{{ printf "%s-%s" .Values.application.name (.Values.global.identifier | lower | replace "." "-") }}
{{- else -}}
{{ .Values.application.name }}
{{- end -}}
{{- end -}}

{{/* Generate application labels */}}
{{- define "application.labels" }}
app: {{ .Values.application.name }}
{{ if eq .Release.Namespace "qa" }}
identifier: {{ .Values.global.identifier | lower | replace "." "-" }}
{{- end -}}
{{- end }}

{{/* Generate application version labels */}}
{{- define "application.version.labels" }}
version: {{ .Chart.AppVersion }}
lastDeploy: {{ date "20060102150405" .Release.Time | quote }}
{{- end }}

{{/* Generate application arguments */}}
{{- define "application.arguments" -}}
--server.port={{ .Values.application.port }} --spring.profiles.active={{ .Values.application.profiles }} {{ .Values.application.arguments }}
{{- end -}}

{{/* Generate application java arguments */}}
{{- define "application.javaArgs" -}}
{{ template "newrelic.javaArgs" . }} -Dlog4j.formatMsgNoLookups=true
{{- end -}}

{{/* Generate newrelic java arguments */}}
{{- define "newrelic.javaArgs" -}}
-javaagent:/newrelic/newrelic.jar -Dnewrelic.config.file=/application/newrelic/newrelic.yml -Dnewrelic.environment={{ .Release.Namespace }}
{{- end -}}

{{/* Generate application liveness probe */}}
{{- define "application.container.livenessProbe" -}}
{{- if .Values.application.livenessProbe }}
livenessProbe:
{{ toYaml .Values.application.livenessProbe | indent 2 }}
{{- end -}}
{{- end -}}

{{/* Generate application liveness readiness */}}
{{- define "application.container.readinessProbe" -}}
{{- if .Values.application.readinessProbe }}
readinessProbe:
{{ tpl (toYaml .Values.application.readinessProbe) . | indent 2 }}
{{- end -}}
{{- end -}}

{{/* Generate application resources */}}
{{- define "application.container.resources" -}}
{{- if .Values.application.resources }}
resources:
{{ tpl (toYaml .Values.application.resources) . | indent 2 }}
{{- end -}}
{{- end -}}

{{/* Generate deployment annotations */}}
{{- define "deployment.annotations" -}}
{{- range $annotation, $value := .Values.deployment.annotations }}
{{ $annotation }}: {{ $value | quote }}
{{- end }}
{{- end }}

{{/* Generate application annotations */}}
{{- define "application.annotations" -}}
{{- range $annotation, $value := .Values.application.annotations }}
{{ $annotation }}: {{ $value | quote }}
{{- end }}
{{- end }}

{{- define "helm.labels" -}}
"app.kubernetes.io/managed-by": "Helm"
{{- end }}

{{- define "helm.annotations" -}}
"meta.helm.sh/release-name": "{{ .Release.Name }}"
"meta.helm.sh/release-namespace": "{{ .Release.Namespace }}"
{{- end }}